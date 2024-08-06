# ReplaceText

This project replaces text in files based on a dictionary, given user input to specify which direction (keys-to-values or values-to-keys).

## Features

- Replace text in files based on dictionaries defined in a configuration file.
- Allows user to specify the direction of replacement (keys-to-values or values-to-keys).
- Allows user to specify which file extensions to ignore.
- Automatically uses the only dictionary if only one is defined in the configuration file.

## Requirements

- Python 3.8 or higher
- Poetry package manager

## Installation

1. **Install Poetry** (if not already installed):

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. **Clone the repository and navigate to the project directory**:

    ```sh
    git clone https://github.com/cainky/ReplaceText.git
    cd ReplaceText
    ```

3. **Install dependencies**:

    ```sh
    poetry install
    ```

## Configuration

1. **Rename the example configuration file**:

    ```sh
    mv example_config.json config.json
    ```

2. **Edit `config.json` to define your dictionaries**. Here is an example

    ```json
    {
      "dictionaries": {
        "example1": {
          "key1": "value1",
          "key2": "value2",
          "key3": "value3"
        },
        "example2": {
          "hello": "world",
          "foo": "bar",
          "python": "rocks"
        }
      },
      "ignore_extensions": [".png", ".jpg", ".gif"]
    }
    ```

## Usage

Run the script using Poetry:

```sh
poetry run python replace_text/replace_text.py
```

The script will prompt you for the following inputs:

Direction of replacement:

- Enter '1' for keys-to-values
- Enter '2' for values-to-keys

Folder path:

- Enter the path to the folder containing the files to be processed.

Dictionary name:

- Enter the name of the dictionary to use from config.json.
The script will process all files in the specified folder, replacing text based on the selected dictionary and direction.

## License
ReplaceText is distributed under the [GNU General Public License, Version 3](./LICENSE), allowing for free software distribution and modification while ensuring that all copies and modified versions remain free.
