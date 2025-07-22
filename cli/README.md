# CLI Tool Documentation

This CLI tool provides a set of commands to help developers manage and deploy their applications efficiently. Below is a list of all available commands in the `cli` directory, organized by functionality.

## Commands
### General Commands
- **Get help on CLI commands**  
  `cx-cli --help`  
  Displays help information for all available commands.

- **Get help on a specific command**
- `cx-cli <command> --help`  
  Displays help information for the specified command.

- **Create metadata**
- `cx-cli init`  
  Creates metadata for the application.

- **validate metadata**
- `cx-cli validate-app`  
  Validates the metadata of the application.


### datafabric Management

- **Deploy a connector**  
  `cx-cli datafabric add-connector`  
  Deploys the specified connector.

- **Destroy a connector**  
  `cx-cli datafabric destroy-connector <connector-name>`  
  Removes the specified connector.

- **List all connectors**  
  `cx-cli datafabric list-connectors`  
  Lists all available connectors.

### API Function Management

- **Get help on API commands**  
  `cx-cli api --help`  
  Displays help information for API-related commands.

- **Create a new function**  
  `cx-cli api add-function`  
  Creates a new API function.

- **Destroy a function**  
  `cx-cli api destroy-function <function-name>`  
  Removes the specified API function.

- **List all functions**  
  `cx-cli api list-functions`  
  Lists all available API functions.


### IAM Management
- **Get help on IAM commands**  
  `cx-cli iam --help`  
  Displays help information for IAM-related commands.

- **Create Permission**
- `cx-cli iam create_permission`  
    Creates a new permission in the IAM system.

- **Create Tenant**
  - `cx-cli iam create_tenant`  
    Creates a new tenant in the IAM system.
  

    
This version is for end-users who want to install and run the CLI from GitHub.

# Lifecycle CLI

Command-line interface tool for managing lifecycle operations.

## 🧩 Installation (via GitHub)

You can install the CLI directly from the GitHub repo:

## bash
pip install git+https://github.com/<your-org>/<your-repo>.git#subdirectory=cli
Make sure you have Python ≥ 3.9 and pip installed.

🚀 Usage

Once installed, you can access the CLI using:

cx-cli --help
Example:

cx-cli init 
cx-cli datafabric add-connector <connector-name>
🔄 Enable Autocomplete (Optional but Recommended)

Typer provides autocomplete for bash, zsh, and fish.

Enable it by running:

cx-cli --install-completion



---

## 🛠️ 2. **README for Developers (Contributors)**

This version is for internal developers who are working on the CLI source code.

# Lifecycle CLI - Developer Guide

## 🧪 Local Setup

Clone the repository and set up Poetry (if you haven’t already):

1. `git clone https://github.com/CXEPI/cxp-lifecycle.git`
2. `cd cxp-lifecycle/cli`
3. `poetry install`
4. copy .env.example to .env and fill in the required environment variables

To run the CLI locally:

1. `poetry run cx-cli --help`

or globally by:

1. `cd cxp-lifecycle/cli`

2. `pip install -e .`

and then just use: `cx-cli` (it will also automatically reflects changes you make in the lifecycle code)

To test a command:

poetry run cx-cli hello --name Dev
🧹 Lint and Format

Run formatting and lint checks:

poetry run black src
🧪 Tests

poetry run pytest
🔄 Releasing a New Version

Bump version in pyproject.toml under [tool.poetry]:
version = "0.2.0"
Commit and push the changes:
git add pyproject.toml
git commit -m "chore: bump CLI version to 0.2.0"
git push
Create a GitHub Release (optional):
Go to GitHub > Releases > Draft a new release
Tag: v0.2.0
Title: v0.2.0
Description: Add change notes
Notify users to update:
pip install --upgrade git+https://github.com/<your-org>/<your-repo>.git#subdirectory=cli
🧠 Autocomplete (for dev testing)

Run once to install CLI autocomplete:

poetry run cx-cli --install-completion
Then restart your shell or source ~/.bashrc.

## 🛠️ Creating a Standalone Executable (.exe) with PyInstaller

You can package the CLI into a single `.exe` for users who don't have Python installed.

### 1. Install PyInstaller

```bash
pip install pyinstaller
2. Add a launcher script
Create src/cli/main.py:

from cli.commands import app

if __name__ == "__main__":
    app()
3. Build the binary
From the cli/ folder:

pyinstaller --onefile src/cli/main.py --name cx-cli --paths src
Output:

dist/cx-cli.exe       # Windows
dist/cx-cli           # Linux/macOS
4. Run the binary
./dist/cx-cli --help
5. Clean up (optional)
Add to .gitignore:

# PyInstaller
build/
dist/
*.spec


🚀 Upload to a GitHub Release (Manual)
To distribute the .exe (or Linux/macOS binary) via GitHub:

Go to the GitHub repo page
Click "Releases" → "Draft a new release"
Fill in:
Tag: v0.2.0 (must match version in pyproject.toml)
Release title: CLI v0.2.0
Description: Add notes on what's new
Attach files:
Click "Attach binaries by dropping them here or selecting them"
Upload dist/cx-cli.exe (or the relevant platform binary)
Click "Publish release"
Now users can download it directly from GitHub.

