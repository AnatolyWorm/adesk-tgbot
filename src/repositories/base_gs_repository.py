import logging

from gspread.spreadsheet import Spreadsheet

from src.core.google_sheets_api import google_sheets_api_service, GoogleSheetsApiService

logger = logging.getLogger(__name__)


class BaseGSRepository(GoogleSheetsApiService):

    def get_rows(
        self,
        sheet_name: str,
        start_col: str,
        end_col: str,
        start_row: int,
        end_row: int | None = '',
    ) -> list[list[str]]:
        worksheet = self.book.worksheet(sheet_name)
        return worksheet.get(f"{start_col}{start_row}:{end_col}{end_row}")

    def save_rows(
        self,
        sheet_name: str,
        data: list[str],
    ) -> bool:
        try:
            worksheet = self.book.worksheet(sheet_name)
            worksheet.append_rows(data, value_input_option='USER_ENTERED')
            return True
        except Exception:
            logger.error('Google cant save data')