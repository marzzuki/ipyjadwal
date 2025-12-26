import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd
from typing import Literal


class Jadwal:
    def __init__(
        self,
        gspread_client,
        sort_method: Literal["default", "asc", "dsc"] = "default",
    ):
        self.gc = gspread_client
        self.sort_method = sort_method
        self.current_spreadsheet = None
        self.file_mapping = {}
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
            description="Refresh",
            button_style="info",
        )

        self.output = widgets.Output()

        self.ui = widgets.VBox(
            [
                widgets.HBox(
                    [
                        self.file_dropdown,
                        self.refresh_btn,
                    ]
                ),
                self.sheet_dropdown,
                self.output,
            ]
        )

        self.refresh_btn.on_click(self.on_refresh_click)
        self.file_dropdown.observe(self.on_file_change, names="value")
        self.sheet_dropdown.observe(self.on_sheet_change, names="value")

        self.refresh_file_list()

    def refresh_file_list(self):
        original_btn_text = self.refresh_btn.description
        self.refresh_btn.description = "Loading..."
        self.refresh_btn.disabled = True

        try:
            files = self.gc.list_spreadsheet_files()
            if self.sort_method == "asc":
                files = sorted(
                    files,
                    key=lambda x: x["name"],
                )
            elif self.sort_method == "dsc":
                files = sorted(
                    files,
                    key=lambda x: x["name"],
                    reverse=True,
                )

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

        with self.output:
            clear_output()
            print(f"📂 Opening '{filename}'...")

            try:
                file_id = self.file_mapping[filename]
                self.current_spreadsheet = self.gc.open_by_key(file_id)

                worksheets = self.current_spreadsheet.worksheets()
                sheet_name = [ws.title for ws in worksheets]

                self.sheet_dropdown.options = sheet_name
                self.sheet_dropdown.disabled = False

                if sheet_name:
                    self.sheet_dropdown.value = sheet_name[0]

            except Exception as e:
                print(f"❌ Error opening file: {e}")

    def on_sheet_change(self, change):
        sheet_name = change["new"]

        if not sheet_name or not self.current_spreadsheet:
            return

        with self.output:
            clear_output()
            print(f"📊 Loading data from '{sheet_name}'...")

            try:
                worksheet = self.current_spreadsheet.worksheet(sheet_name)
                rows = worksheet.get_all_values()

                if rows:
                    df = pd.DataFrame(rows[1:], columns=rows[0])
                    print(f"✅ Loaded {len(df)} rows.")
                    display(df.head())
                else:
                    print("⚠️ This sheet is empty.")
            except Exception as e:
                print(f"❌ Error reading sheet: {e}")

    def show(self):
        display(self.ui)
