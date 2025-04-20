To obtain the full test coverage for the project, you need to execute the following commands:

1. Run the tests while ignoring specific files:
    ```bash
    pytest --ignore=tests/test_contract.py --ignore=tests/test_cli.py --cov=data_sitter
    ```

2. Run the ignored tests separately and append their coverage:
    ```bash
    pytest tests/test_contract.py tests/test_cli.py --cov=data_sitter --cov-append
    ```

If you need to generate an HTML report of the coverage, execute the following command after running the tests:

```bash
coverage html
```
