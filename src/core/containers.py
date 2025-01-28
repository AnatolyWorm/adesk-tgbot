from dishka import provide, Scope, Provider, make_container

from src.core.google_sheets_api import GoogleSheetsApiService, google_sheets_api_service
# from src.core.redis import UrlRedis
from src.core.settings import SheetNames, Settings, settings

from repositories.handbook import HandBookRepository


class Container(Provider):

    @provide(scope=Scope.APP)
    def get_google_sheet(self) -> GoogleSheetsApiService:
        return GoogleSheetsApiService(
            creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
            sheet_id=settings.GOOGLE_SPREADSHEET_ID,
        )

    @provide(scope=Scope.REQUEST)
    def get_handbook_repo(self) -> HandBookRepository:
        return HandBookRepository(
            spread_sheet_name=settings.GOOGLE_SPREADSHEET_NAMES.handbook,
            workbook=google_sheets_api_service,
        )


container = Container()
