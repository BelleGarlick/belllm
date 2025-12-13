import subprocess


def run() -> str:
    """This function is used to call amazon's internal build system: brazil-build.

    :return: A small message with the status of calling brazil-build.
    """
    try:
        print("Calling brazil build")
        result = subprocess.run(
            ["brazil-build"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout  # Store the output in a variable
        print("Output:", output)

        return "Build"
    except subprocess.CalledProcessError as e:
        return "Calling brazil-build failed: " + str(e)
