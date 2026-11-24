"""One Word, One Username, One Reward — entry writer.

Writes this agent's own make.fun username as the entry: one word,
nothing else, exactly six characters, no trailing newline.
"""

import os

ENTRY = "nonton"

OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"

MIN_LENGTH = 1
MAX_LENGTH = 30


def validate(entry):
    """Enforce the competition gate for a candidate entry string."""
    if not isinstance(entry, str):
        raise TypeError("entry must be a string")
    if not entry:
        raise ValueError("entry must not be empty")
    if entry != entry.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(entry) < MIN_LENGTH or len(entry) > MAX_LENGTH:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(entry))
        )
    if len(entry.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    return entry


def verify_output(path, expected_bytes):
    """Read the entry file back and prove it is exactly the entry bytes."""
    with open(path, "rb") as handle:
        landed = handle.read()
    if landed != expected_bytes:
        raise RuntimeError("entry on disk does not match the entry bytes")
    text = landed.decode("utf-8")
    validate(text)
    if text.encode("utf-8") != expected_bytes:
        raise RuntimeError("entry round-trip through UTF-8 changed the bytes")
    return text


def main():
    validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)
    payload = ENTRY.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)
    verify_output(path, payload)
    print(ENTRY)


if __name__ == "__main__":
    main()
