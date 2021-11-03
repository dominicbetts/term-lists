## Experiments to generate different versions of term lists from a YAML source file.

The intention is to generate different versions of the term list for different audiences, for example internal and external.

The term list used in this repository is based on this published glossary: [Glossary of IoT terms](https://docs.microsoft.com/en-us/azure/iot-fundamentals/iot-glossary).

Currently, the Python [script](parse-term-list.py) regenerates the published glossary and contributor guide term list from the YAML source.

- Requires Python 3 and the `regex` and `slugify` modules - use the VS Code extension for debugging: https://marketplace.visualstudio.com/items?itemName=ms-python.python
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


## To do and next steps

- Make sure that automatic cross-linking works for acronymns as well as full terms.
- Some kind of validation on "See also" entries - although errors are picked up when the markdown is submitted in a PR.
- Linking needs work. We want to use relative or site relative links for "learn more" and manual links in definition, but the generated links may need to different for customer facing glossaries as compared to internal term lists.
- Can the schema and setting be packaged in a VS Code extension?