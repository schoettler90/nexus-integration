# nexus-integration

## Prerequisites

### Install Python 3.13

#### Windows

1. Download Python 3.13 from the official website:
   - Visit [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Download the latest Python 3.13.x installer for Windows

2. Run the installer:
   - **Important**: Check "Add Python 3.13 to PATH" during installation
   - Click "Install Now" or choose "Customize installation" for advanced options

3. Verify the installation:
   ```powershell
   python --version
   ```
   Should output: `Python 3.13.x`

#### macOS

Using Homebrew:
```bash
brew install python@3.13
```

Or download from [python.org](https://www.python.org/downloads/)

#### Linux

Using apt (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

Using dnf (Fedora):
```bash
sudo dnf install python3.13
```

### Install Poetry

Poetry is a dependency management and packaging tool for Python.

#### Windows (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

After installation, add Poetry to your PATH if not automatically added:
- The installer will show the path to add (typically `%APPDATA%\Python\Scripts`)

#### macOS/Linux

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Verify Poetry Installation

```powershell
poetry --version
```

#### Configure Poetry (Optional)

To create virtual environments inside the project directory:
```powershell
poetry config virtualenvs.in-project true
```

## Setup

1. Clone the repository:
   ```powershell
   git clone <repository-url>
   cd nexus-integration
   ```

2. Install dependencies:
   ```powershell
   poetry install
   ```

3. Activate the virtual environment:
   ```powershell
   poetry shell
   ```

## Usage

*Add usage instructions here*


