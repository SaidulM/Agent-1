name: Agent1-Research
on:
  repository_dispatch:
    types: [agent1_trigger]

jobs:
  run-agent1:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install requests google-api-python-client

      - name: Run Agent1 script
        run: python agent1.py
