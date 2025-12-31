def read_md(filepath: str) -> str:
    """
    Reads the contents of a Markdown (.md) file from the given filepath and returns it as a string.

    Args:
        filepath (str): The path to the Markdown file.

    Returns:
        str: The content of the Markdown file as a string.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content
