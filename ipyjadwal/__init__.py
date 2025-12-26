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
                print(f"❌ List Error: {e}")
        finally:
            self.refresh_btn.disabled = False

    def on_refresh_click(self, b):
        current_file = self.file_dropdown.value
        current_sheet = self.sheet_dropdown.value

        with self.output:
            clear_output(wait=True)
            print("🔄 Refreshing Drive list...")
            self.refresh_file_list()

        if current_file:
            self._load_spreadsheet(current_file, last_sheet_to_restore=current_sheet)

    def on_file_change(self, change):
        if change["new"] and change["new"] in self.file_mapping:
            self._load_spreadsheet(change["new"])

    def _load_spreadsheet(self, filename, last_sheet_to_restore=None):
        self.sheet_dropdown.unobserve(self.on_sheet_change, names="value")
        self.sheet_dropdown.disabled = True

        with self.output:
            clear_output(wait=True)
            print(f"📂 Syncing '{filename}'...")
            try:
                file_id = self.file_mapping[filename]

                print("   ↪️ Connecting to Google API...")
                self.spreadsheet = self.gc.open_by_key(file_id)

                print("   ↪️ Fetching worksheets...")
                worksheets = self.spreadsheet.worksheets()
                sheet_names = [ws.title for ws in worksheets]

                self.sheet_dropdown.options = sheet_names
                self.sheet_dropdown.disabled = False

                if last_sheet_to_restore in sheet_names:
                    self.sheet_dropdown.value = last_sheet_to_restore
                elif sheet_names:
                    self.sheet_dropdown.value = sheet_names[0]

                self.sheet_dropdown.observe(self.on_sheet_change, names="value")
                self.on_sheet_change({"new": self.sheet_dropdown.value})

            except Exception as e:
                print(f"❌ API Hang or Error: {e}")
                self.sheet_dropdown.observe(self.on_sheet_change, names="value")

    def on_sheet_change(self, change):
        sheet_name = change["new"]
        if not sheet_name or not self.spreadsheet:
            return

        with self.output:
            clear_output(wait=True)
            print(f"📊 Loading worksheet: '{sheet_name}'...")
            try:
                self.sheet = self.spreadsheet.worksheet(sheet_name)
                rows = self.sheet.get_all_values()
                if rows:
                    self.df = pd.DataFrame(rows[1:], columns=rows[0])
                    print(f"✅ Success: {len(self.df)} rows loaded.")
                    display(self.df.head())
                else:
                    self.df = pd.DataFrame()
                    print("⚠️ Note: This sheet is empty.")
            except Exception as e:
                print(f"❌ Worksheet Error: {e}")

    def show(self):
        display(self.ui)
