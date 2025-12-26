# ipyjadwal 📊

[![PyPI version](https://badge.fury.io/py/ipyjadwal.svg?cache=v1)](https://badge.fury.io/py/ipyjadwal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/ipyjadwal.svg?cache=v1)](https://pypi.org/project/ipyjadwal/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**ipyjadwal** (derived from the Arabic *Jadwal* جَدْوَل meaning "Table" or "Schedule") is a clean, interactive Jupyter widget for browsing Google Sheets directly inside **Google Colab** or **Jupyter Notebooks**.

It simplifies the workflow of selecting spreadsheets, switching sheets, and previewing DataFrames without writing repetitive boilerplate code.

## Installation

```bash
pip install ipyjadwal
```

## Usage

```python
import ipyjadwal

widget = ipyjadwal.Jadwal()
widget.show()

# Access selected data as pandas DataFrame
df = widget.df

# Write updates back using gspread
widget.sheet.update_cell(1, 1, "New Value")
```

For local Jupyter Notebooks, provide a gspread client:

```python
import gspread
import ipyjadwal

gc = gspread.service_account("credentials.json")
widget = ipyjadwal.Jadwal(client=gc)
widget.show()
```

## ✨ Features

- **🔍 Interactive Dropdown**  
  Browse all your Google Drive spreadsheets through a clean, searchable dropdown interface.

- **📑 Seamless Sheet Navigation**  
  Automatically loads and displays all available worksheets when you select a spreadsheet—no manual loading required.

- **🐼 Live DataFrame Preview**  
  Instantly preview your data as a pandas DataFrame with automatic updates as you switch between sheets.

- **📊 Full Data Access**  
  Access the complete sheet data via `widget.df` for analysis, transformations, and visualization.

- **✏️ Full gspread Access**  
  Access all gspread functionality via `widget.sheet` (e.g., update cells, append rows, format ranges).

- **🔄 One-Click Refresh**  
  Reload your file list or refresh sheet data with a single button click.

- **🔀 Flexible Sorting**  
  Sort spreadsheets by name (ascending/descending) or leave untouched to preserve Google Sheets' default order.

- **🎯 Zero Boilerplate**  
  Skip repetitive setup code—import, instantiate, and start exploring your data immediately.

## 🔧 Documentation

### API Reference

#### `Jadwal(client=None, sort_method="default")`

Main widget class for browsing Google Sheets.

**Parameters**

- `client` (optional): An authorized gspread client. If `None`, attempts automatic authentication in Google Colab.
- `sort_method`: `"default"` (default), `"asc"`, or `"dsc"` — Sort order for the file list.

**Properties**

- `df`: pandas DataFrame containing the full data from the currently selected sheet.
- `sheet`: gspread worksheet object for the currently selected sheet — use this to write back to Google Sheets.

**Methods**

- `show()`: Display the interactive widget.

## Links

- [PyPI Package](https://pypi.org/project/ipyjadwal/)
- [GitHub Repository](https://github.com/marzzuki/ipyjadwal)
- [Issue Tracker](https://github.com/marzzuki/ipyjadwal/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [gspread](https://github.com/burnash/gspread) for Google Sheets API
- Powered by [ipywidgets](https://ipywidgets.readthedocs.io/) for interactive UI
