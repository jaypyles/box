import subprocess
from enum import Enum


class Shell(Enum):
    BASH = "bash"
    FISH = "fish"


def execute_command(command: str, shell: Shell = Shell.FISH):
    result = subprocess.run(
        [shell.value, "-c", command],
        capture_output=True,
        text=True,
    )

    if shell == Shell.FISH:
        if "\n" in result.stdout:
            result.stdout = result.stdout.split("\n", 1)[1]

    return result.stdout.strip(), result.stderr.strip()
