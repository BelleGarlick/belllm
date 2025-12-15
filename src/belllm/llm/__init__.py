import belllm.plugins
from belllm import config
from belllm.chats.models import Chat, ChatMessages, Message
from belllm.llm.models import LlmResponse, LlmPluginContext
from belllm.utils import get_root_dir
import belllm.context


def _call_llm(tools, messages: ChatMessages) -> LlmResponse:
    agent_type = config.get("agent.type")

    if agent_type == "ollama":
        from belllm.llm import ollama_api

        return ollama_api.call(
            tools=tools,
            messages=messages
        )

    raise ValueError(f"Unknown agent type: {agent_type}")


def _call_llm_with_tools(tools, messages: ChatMessages):
    # todo change so only added once per chat instance
    full_messages = []

    global_context_message = belllm.context.get_system_message_for_global_context()
    if global_context_message:
            full_messages.append(Message(
                role="system",
                content=global_context_message
            ))

    for tool in belllm.plugins.get_prechat_script():
        content = tool["run"]()
        if content:
            full_messages.append(Message(
                role="system",
                tool_name=tool["name"],
                content=content
            ))

    full_messages = [*full_messages, *messages]

    response = _call_llm(
        messages=full_messages,
        tools=tools
    )

    if response.tool_calls:
        for call in response.tool_calls:
            tool = belllm.plugins.get_library().get(call.function.name)
            tool['function'].__globals__['ctx'] = LlmPluginContext(
                global_user_data_path=get_root_dir(),
                call_llm=lambda input_message: _call_llm(
                    messages=[Message(role="user", content=input_message)],
                    tools=[]
                ).content
            )
            result = tool["function"](**call.function.arguments)

            # todo have callback for permissions and whatnot

            messages.append(Message(role="tool", tool_name=call.function.name, content=str(result)))

        return _call_llm_with_tools(tools, messages)

    messages.append(Message(role="assistant", content=response.content))

    return response


def chat(request: Chat):
    tools = []
    for tool_name, tool_desc in belllm.plugins.get_library().items():
        props = {}
        required_props = []
        for prop in tool_desc["annotations"]:
            if prop == "return": continue

            props[prop] = {
                "type": str(tool_desc["annotations"][prop])
                # TODO Add description here
            }
            if 'None' not in str(tool_desc["annotations"][prop]):
                required_props.append(prop)

        tools.append({
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_desc['description'],
                "parameters": {
                    "type": "object",
                    "required": required_props,
                    "properties": props
                }
            }
        })

    llm_response = _call_llm_with_tools(tools, request.messages)
    # print("stream thinking or whatever maybe")

    return chat