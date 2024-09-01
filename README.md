# keys-ai-bot-friday

Keys AI bot (Friday)

- [keys-ai-bot-friday](#keys-ai-bot-friday)
  - [Developer Notes](#developer-notes)
  - [User Guide](#user-guide)
    - [Setup](#setup)
    - [Launch Friday](#launch-friday)
      - [Friday Command Line Interface (CLI)](#friday-command-line-interface-cli)
      - [Friday User Interface (UI)](#friday-user-interface-ui)

## Developer Notes

VS Code Profile

- Several VS Code extensions and settings are used for standardization and linting purposes.
- The latest version of the code profile is maintained in the repository under
  [.vscode/Keys DEV.code-profile](.vscode/Keys%20DEV.code-profile)

## User Guide

### Setup

Install latest version of Friday from the repository using pip or poetry.

> [!NOTE]
> Friday expects .env file or mandatory env variable `GOOGLE_API_KEY` and optional `FRIDAY_LOG_DIR` variable.

### Launch Friday

#### Friday Command Line Interface (CLI)

Friday CLI can be launched from CLI using the below command,

```bash
poetry run friday_cli
```

#### Friday User Interface (UI)

Friday UI can be launched from CLI using the below command,

```bash
poetry run friday_gui
```
