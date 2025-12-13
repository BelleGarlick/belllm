from belllm.utils import get_root_dir


MEMORY_BANK_PATH = get_root_dir() / "memory-bank.txt"


def get_memory_bank():
    if MEMORY_BANK_PATH.exists():
        with open(MEMORY_BANK_PATH, "r") as f:
            return f.read()
    return None

# todo should turn this into back to regular plugin and allow for prefixing the memory bank at the start. also store with key value so we can load it each time

def save_to_memory_bank(content: str):
    """Save a message in the memory bank such that it will be given to an llm. This should be used
    as it may provide usful context to the llm. Don't save everything, but save things that are
    general and applicable to the user that may be useful for future prompts. Any information you
    learn about the used should be stored such that the LLM can use it to know about the user.

    Important: This will be given to an llm to remember to frame it in the context of the user

    Args:
        content: The message being saved. This should be in the format that it can be
            used to instruct an LLM.

    Returns:
        Ok if save was successful or the error message otherwise. Repeated executions of a failure may not work.
    """
    print("Memory saved!", content)

    with open(MEMORY_BANK_PATH, "a+") as f:
        f.write(content + "\n")

    return "Saved!"

