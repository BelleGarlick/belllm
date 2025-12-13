import belllm.plugins
from belllm import config
from belllm.chats.models import Chat, ChatMessages, Message
from belllm.llm.models import LlmResponse, LlmPluginContext
from belllm.plugins.memory_bank import get_memory_bank
from belllm.utils import get_root_dir


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
    full_messages = [Message(role="tool", tool_name="memory-bank", content=get_memory_bank()), *messages]

    response = _call_llm(
        messages=full_messages,
        tools=tools
    )

    if response.tool_calls:
        for call in response.tool_calls:
            tool = belllm.plugins.library.get(call.function.name)
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
    if belllm.plugins.library is None:
        belllm.plugins.initialise_plugins()

    tools = []
    for tool_name, tool_desc in belllm.plugins.library.items():
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