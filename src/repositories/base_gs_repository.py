import logging

from gspread.spreadsheet import Spreadsheet

from src.core.google_sheets_api import google_sheets_api_service, GoogleSheetsApiService

logger = logging.getLogger(__name__)


class BaseGSRepository:
    def __init__(
        self,
        spread_sheet_name: str,
        workbook: GoogleSheetsApiService = google_sheets_api_service,
    ):
        self.spread_sheet = workbook.book.worksheet(spread_sheet_name)

    def get_rows(
        self,
        start_col: str,
        end_col: str,
        start_row: int,
        end_row: int | None = '',
    ) -> list[list[str]]:
        return self.spread_sheet.get(f"{start_col}{start_row}:{end_col}{end_row}")

    def save_rows(
        self,
        data: list[str],
    ) -> bool:
        try:
            self.spread_sheet.append_rows(data, value_input_option='USER_ENTERED')
            return True
        except Exception:
            logger.error('Google cant save data')