from dishka import provide, Scope, Provider, make_container

from src.core.google_sheets_api import GoogleSheetsApiService
# from src.core.redis import UrlRedis
from src.core.settings import settings, SheetNames

from repositories.handbook import HandBookRepository


    # spread_sheet_name = provide(SheetNames, scope=Scope.REQUEST)
    # redis_db = provide(UrlRedis)
class Container(Provider):
    scope = Scope.REQUEST

    # google_sheet = provide(GoogleSheetsApiService)
    # handbook = provide(HandBookRepository)

    @provide
    def get_google_sheet(self) -> GoogleSheetsApiService:
        return GoogleSheetsApiService(
            creds_file=settings.GOOGLE_SPREADSHEET_CREDENTIALS_JSON_PATH,
            sheet_id=settings.GOOGLE_SPREADSHEET_ID,
        )

    @provide
    def get_handbook_repo(self, google_sheet: GoogleSheetsApiService) -> HandBookRepository:
        return HandBookRepository(
            book=google_sheet.book,
            spread_sheet_name=settings.GOOGLE_SPREADSHEET_NAMES.handbook
        )

    # @provide
    # def get_google_repo(self):
    #     return self.google_sheet


container = make_container(Container())
