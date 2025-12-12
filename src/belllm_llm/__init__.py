import subprocess

def chat_to_llm(message: str):
    # Run Ollama and pass the message via stdin
    args = ["ollama", "run", "gemma3:4b"]
    print("Running:", " ".join(args))

    process = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,   # allow sending input
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Send the message and get output
    stdout, stderr = process.communicate(input=message.encode())

    if stderr:
        print("Error:", stderr.decode())

    response = stdout.decode()
    print("Response:", response)


if __name__ == "__main__":
    chat_to_llm("Hello")