# keys-ai-bot-friday

Keys AI bot (Friday)

## Developer Notes

- VS Code Profile
  - Several VS Code extensions and settings are used for standardization and linting purposes.
  - The latest version of the code profile is maintained in the repository under
  [.vscode/Keys DEV.code-profile](.vscode/Keys%20DEV.code-profile)

## User Guide

- Friday Bot can be cloned from the GitHub source [[Friday]](https://github.com/shangar-t-a/keys-ai-bot-friday).

- Clone the repository

  ```bash
  git clone https://github.com/shangar-t-a/keys-ai-bot-friday -b main
  ```

- While in development environment, make sure to install friday dependencies. The project can be installed via

  ```bash
  poetry install
  ```

- Friday CLI can be launched from CLI using one of the below commands,

  ```bash
  poetry run friday

  poetry run python friday\main.py
  ```

- [***NOTE***]: Friday expects .env file or mandatory env variable `GOOGLE_API_KEY` and optional `FRIDAY_LOG_DIR`
  variable.
