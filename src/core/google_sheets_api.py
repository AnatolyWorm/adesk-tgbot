import gspread
import logging

from src.core.settings import settings

logger = logging.getLogger(__name__)


class GoogleSheetsApiService:
    def __init__(
        self,
        creds_file: str,
        sheet_id: str,
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


google_sheets_api_service = GoogleSheetsApiService(
    creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
    sheet_id=settings.GOOGLE_SPREADSHEET_ID,
)
