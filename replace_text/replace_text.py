import os
import json
from typing import Dict, List
import click


@click.command(name="replace_text")
@click.option(
    "--direction",
    type=click.IntRange(1, 2),
    prompt="Direction (1 for keys-to-values or 2 for values-to-keys)",
    help="Specify the direction for replacement: 1 for keys-to-values, 2 for values-to-keys.",
)
@click.option(
    "--folder", prompt="Folder path", help="Path to the folder containing text files."
)
@click.option(
    "--dict-name",
    default=None,
    help="Name of the dictionary to use from config.json.",
)
def replace_text(direction: int, folder: str, dict_name: str) -> None:
    """
    Replace text in files based on the given dictionary and direction.

    Args:
        direction (int): Direction for replacement (1 for keys-to-values, 2 for values-to-keys).
        folder (str): Path to the folder containing text files.
        dict_name (str): Name of the dictionary to use from config.json.
    """
    # Load dictionaries and ignore extensions from config file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Retrieve the dictionaries and ignore extensions
    dictionaries = config.get("dictionaries", {})
    ignore_extensions = config.get("ignore_extensions", [])

    if not dictionaries:
        print("No dictionaries found in config.json")
        return

    if dict_name is None:
        if len(dictionaries) == 1:
            dict_name = next(iter(dictionaries))
            print(f"Automatically using the only dictionary available: {dict_name}")
        else:
            dict_name = click.prompt(
                "Dictionary name", type=click.Choice(dictionaries.keys())
            )

    if dict_name not in dictionaries:
        print(f"Dictionary {dict_name} not found in config.json")
        return

    replacement_dict: Dict[str, str] = dictionaries[dict_name]

    if direction == 2:
        replacement_dict = {v: k for k, v in replacement_dict.items()}

    # Process each file in the folder
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.endswith(ext) for ext in ignore_extensions):
                print(f"Skipped file (ignored extension): {file_path}")
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            for key, value in replacement_dict.items():
                content = content.replace(key, value)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Processed file: {file_path}")


if __name__ == "__main__":
    replace_text()
