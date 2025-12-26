import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd
import gspread
from google.auth import default
from typing import Literal, Optional


class Jadwal:
    def __init__(
        self,
        client: Optional[object] = None,
        sort_method: Literal["default", "asc", "dsc"] = "default",
    ):
        """
        Args:
            client: (Optional) An authorized gspread client.
                    If None, attempts to authenticate via Google Colab.
            sort_method: Sort order for file list ('default', 'asc', 'dsc').
        """
        self.sort_method = sort_method

        if client:
            self.gc = client
        else:
            self.gc = self._authenticate_colab()

        # --- Public Properties ---
        self.spreadsheet = None
        self.sheet = None
        self.df = None
        self.file_mapping = {}

        # --- UI Components ---
        self.file_dropdown = widgets.Combobox(
            placeholder="Select a Spreadsheet...",
            description="<b>File:</b>",
            ensure_option=True,
            layout={"width": "400px"},
        )

        self.sheet_dropdown = widgets.Dropdown(
            description="<b>Sheet:</b>",
            disabled=True,
            layout={"width": "400px"},
        )

        self.refresh_btn = widgets.Button(
            description="Refresh", button_style="info", icon="refresh"
        )

        self.output = widgets.Output()

        self.ui = widgets.VBox(
            [
                widgets.HBox([self.file_dropdown, self.refresh_btn]),
                self.sheet_dropdown,
                self.output,
            ]
        )

        # --- Bind Events ---
        self.refresh_btn.on_click(self.on_refresh_click)
        self.file_dropdown.observe(self.on_file_change, names="value")
        self.sheet_dropdown.observe(self.on_sheet_change, names="value")

        if self.gc:
            self.refresh_file_list()

    def _authenticate_colab(self):
        """Internal helper to handle Colab authentication automatically."""
        try:
            from google.colab import auth

            print("🔐 Authenticating with Google Colab...", end="\r")
            auth.authenticate_user()
            creds, _ = default()
            gc = gspread.authorize(creds)
            print("✅ Authenticated successfully.      ")
            return gc

        except ImportError:
            raise ImportError(
                "❌ Could not import 'google.colab'. \n"
                "You are likely running outside of Colab.\n"
                "Please provide a gspread client manually:\n\n"
                "   import gspread\n"
                "   gc = gspread.service_account('path/to/creds.json')\n"
                "   widget = Jadwal(client=gc)"
            )
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return None

    def refresh_file_list(self):
        if not self.gc:
            return

        original_btn_text = self.refresh_btn.description
        self.refresh_btn.description = "Loading..."
        self.refresh_btn.disabled = True

        try:
            files = self.gc.list_spreadsheet_files()
            if self.sort_method == "asc":
                files = sorted(files, key=lambda x: x["name"])
            elif self.sort_method == "dsc":
                files = sorted(files, key=lambda x: x["name"], reverse=True)

            self.file_mapping = {f["name"]: f["id"] for f in files}
            self.file_dropdown.options = list(self.file_mapping.keys())
        except Exception as e:
            with self.output:
                print(f"❌ Error fetching files: {e}")
        finally:
            self.refresh_btn.description = original_btn_text
            self.refresh_btn.disabled = False

    def on_refresh_click(self, b):
        self.refresh_file_list()
        if self.file_dropdown.value:
            self.on_file_change({"new": self.file_dropdown.value})

    def on_file_change(self, change):
        filename = change["new"]
        if not filename or filename not in self.file_mapping:
            return

        self.sheet_dropdown.disabled = True
        self.sheet_dropdown.options = []
        self.sheet = None
        self.df = None

        with self.output:
            clear_output()
            print(f"📂 Opening '{filename}'...")

            try:
                file_id = self.file_mapping[filename]
                self.spreadsheet = self.gc.open_by_key(file_id)

                worksheets = self.spreadsheet.worksheets()
                sheet_names = [ws.title for ws in worksheets]

                self.sheet_dropdown.options = sheet_names
                self.sheet_dropdown.disabled = False

                if sheet_names:
                    self.sheet_dropdown.value = sheet_names[0]

            except Exception as e:
                print(f"❌ Error opening file: {e}")

    def on_sheet_change(self, change):
        sheet_name = change["new"]

        if not sheet_name or not self.spreadsheet:
            return

        with self.output:
            clear_output()
            print(f"📊 Loading data from '{sheet_name}'...")

            try:
                self.sheet = self.spreadsheet.worksheet(sheet_name)
                rows = self.sheet.get_all_values()

                if rows:
                    self.df = pd.DataFrame(rows[1:], columns=rows[0])
                    print(f"✅ Loaded {len(self.df)} rows.")
                    print("💡 Access data via: widget.df")
                    display(self.df.head())
                else:
                    self.df = pd.DataFrame()
                    print("⚠️ This sheet is empty.")
            except Exception as e:
                self.df = None
                self.sheet = None
                print(f"❌ Error reading sheet: {e}")

    def show(self):
        display(self.ui)
