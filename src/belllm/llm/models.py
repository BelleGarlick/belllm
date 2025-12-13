from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any


@dataclass
class LlmResponse:

    tool_calls: Any

    content: str

    thinking: str | None


@dataclass
class LlmPluginContext:

    global_user_data_path: Path

    call_llm: Callable[[str], str]
