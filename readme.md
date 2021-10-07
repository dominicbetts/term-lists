## Experiments to generate different versions of term lists from a YAML source file.

The intention is to generate different versions of the term list for different audiences, for example internal and external.

The term list used in this repository is based on this published glossary: [Glossary of IoT terms](https://docs.microsoft.com/en-us/azure/iot-fundamentals/iot-glossary).

Currently, the Python [script](parse-term-list.py) regenerates the published glossary from the YAML source. *Next step is to generate a version of the term list for the contributor guide.*

- Requires Python 3 and the `regex` module - use the VS Code extension for debugging: https://marketplace.visualstudio.com/items?itemName=ms-python.python
- To run the script:

    ```
    python3 parse-term-list.py full-iot-term-list.yaml customer-facing
    ```

Also includes a YAML [schema](term-list.schema.json) to assist editing the YAML term list in VS Code:

- YAML schema relies on the YAML extension: https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml
- Settings in VS Code look like:

    ```
    "yaml.schemas": {
        "./term-list.schema.json": [
            "*-term-list.yaml"
        ]
    }
    ```
