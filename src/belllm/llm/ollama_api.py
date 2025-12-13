from ollama import chat

from belllm import config
from belllm.chats.models import ChatMessages
from belllm.llm.models import LlmResponse


def call(tools, messages: ChatMessages):
    model_name = config.get("agent.model")
    thinking_enabled = config.get("agent.think", False)

    response = chat(
        model=model_name,
        messages=[x.model_dump() for x in messages],
        tools=tools,
        think=thinking_enabled
    ).message

    return LlmResponse(
        tool_calls=response.tool_calls,
        thinking=response.thinking,
        content=response.content
    )