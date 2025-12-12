from ollama import chat

# todo expand on this and plugins and whatnot


if __name__ == "__main__":
    import belllm

    belllm.plugins.initialise_plugins()

    full_tool_chain = []
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

        full_tool_chain.append({
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

    messages = [{"role": "user", "content": "Please create a workout in tidalflow. then confirm the id of the workout"}]
    print("caaling api")
    # pass functions directly as tools in the tools list or as a JSON schema
    response = chat(
        model="qwen3-vl:4b",
        messages=messages,
        tools=full_tool_chain,
        think=False
    )

    print(response)

    messages.append(response.message)
    if response.message.tool_calls:
        print(response.message.tool_calls)
        # only recommended for models which only return a single tool call
        call = response.message.tool_calls[0]
        tool = belllm.plugins.library.get(call.function.name)
        result = tool["function"](**call.function.arguments)

        print(result)

        # add the tool result to the messages
        messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

        final_response = chat(
            model="qwen3-vl:4b",
            messages=messages,
            tools=full_tool_chain,
            think=False
        )

        print(final_response.message.content)


