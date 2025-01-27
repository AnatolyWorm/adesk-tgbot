import gspread
import logging

from src.core.settings import settings

logger = logging.getLogger(__name__)


class GoogleSheetsApiService:
    def __init__(
        self,
        creds_file: str = settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
        sheet_id: str = settings.GOOGLE_SPREADSHEET_ID,
    ):
        if not creds_file:
            logger.error('GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH is not set')
            return
        if not sheet_id:
            logger.error('GOOGLE_SPREADSHEET_ID is not set')
            return
        try:
            spreadsheet = gspread.service_account(
                filename=creds_file
            )
        except Exception as x:
            logger.exception(x)
            
        self.book = spreadsheet.open_by_key(sheet_id)

    # def get_rows_by_sheetname(
    #     self,
    #     sheet_name: str,
    #     start_col: str,
    #     end_col: str,
    #     start_row: int,
    #     end_row: int | None = '',
    # ) -> list[list[str]]:
    #     worksheet = self.book.worksheet(sheet_name)
    #     return worksheet.get(f"{start_col}{start_row}:{end_col}{end_row}")

    # def save_rows(
    #     self,
    #     sheet_name: str,
    #     data: list[str],
    # ) -> bool:
    #     try:
    #         worksheet = self.book.worksheet(sheet_name)
    #         worksheet.append_rows(data, value_input_option='USER_ENTERED')
    #         return True
    #     except Exception:
    #         logger.error('Google cant save data')


google_sheets_api_service = GoogleSheetsApiService(
    creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
    sheet_id=settings.GOOGLE_SPREADSHEET_ID,
)
