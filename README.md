# ipyjadwal 📊

[![PyPI version](https://badge.fury.io/py/ipyjadwal.svg)](https://badge.fury.io/py/ipyjadwal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/ipyjadwal.svg)](https://pypi.org/project/ipyjadwal/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**ipyjadwal** (derived from the Arabic *Jadwal* جَدْوَل meaning "Table" or "Schedule") is a clean, interactive Jupyter widget for browsing Google Sheets directly inside **Google Colab** or **Jupyter Notebooks**.

It simplifies the workflow of selecting spreadsheets, switching sheets, and previewing DataFrames without writing repetitive boilerplate code.

## 🚀 Quick Start

### Installation

```bash
pip install ipyjadwal
```

### Basic Usage

ipyjadwal handles the UI, but you must provide the authentication (standard for security reasons).

```python
from google.colab import auth
from google.auth import default
import gspread
import ipyjadwal

# 1. Authenticate with Google
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# 2. Launch the Jadwal widget
widget = ipyjadwal.Jadwal(gc)
widget.show()
```

For **Jupyter Notebooks** (local), you'll need to set up your Google credentials file:

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ipyjadwal

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(creds)

widget = ipyjadwal.Jadwal(gc)
widget.show()
```


## ✨ Features

- **🔍 Dropdown Interface**  
  Browse your Google Drive spreadsheets using a searchable dropdown menu.

- **📑 Instant Sheet Switching**  
  Automatically loads available worksheets when a file is selected.

- **🐼 Pandas Preview**  
  Instantly preview the head of the selected sheet as a Pandas DataFrame.

- **🔄 Refresh Capability**  
  Reload your file list or sheet data with a single click.

- **🎯 Zero Boilerplate**  
  No need to write repetitive code for browsing and switching between sheets.

## 🔧 Documentation

### API Reference

#### `Jadwal(gc)`

Main widget class for browsing Google Sheets.

**Parameters:**
- `gc` (gspread.Client): An authorized gspread client instance

**Methods:**
- `show()`: Display the interactive widget

**Example:**

```python
widget = ipyjadwal.Jadwal(gc)
widget.show()
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📞 Support

If you encounter any issues or have questions, please:
- Open an issue on [GitHub Issues](https://github.com/yourusername/ipyjadwal/issues)
- Check existing issues and discussions


## 🙏 Acknowledgments

- Built with [gspread](https://github.com/burnash/gspread) for Google Sheets API
- Powered by [ipywidgets](https://ipywidgets.readthedocs.io/) for interactive UI

## 🔗 Links

- [PyPI Package](https://pypi.org/project/ipyjadwal/)
- [GitHub Repository](https://github.com/marzzuki/ipyjadwal/issues)
- [Issue Tracker](https://github.com/marzzuki/ipyjadwal/issues)
