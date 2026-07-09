# ⚙️ Installation & Setup

This page guides you through the process of setting up and running HECTOR-Editor on your system.

## System Requirements
* **Python 3.8 or higher**
* Active internet connection (only required for querying external authority APIs like Wikidata, Getty AAT, and GND).

## Installation

1. **Clone the Repository:**
   Clone the code to your local machine:
   ```bash
   git clone https://github.com/bcdhbonn/hector-editor-skos.git
   cd hector-editor-skos
   ```

2. **Install Dependencies:**
   Install the required libraries listed in `requirements.txt` via pip:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: CustomTkinter relies on Pillow (PIL) for image assets, which is installed automatically as part of its dependencies.*

## Launching the Editor

You can launch the application by running the main Python file:
```bash
python hector_editor.py
```

## Building Standalone Executable (Optional)

If you wish to bundle the HECTOR-Editor into a single executable file (e.g. `hector_editor.exe` on Windows), you can use PyInstaller with the provided spec file:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the application:
   ```bash
   pyinstaller hector_editor.spec
   ```
The compiled output will be generated inside the `dist/` directory, complete with the embedded application logo and CustomTkinter configuration.
