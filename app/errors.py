
class CustomHttpExc(Exception):
    def __init__(self, details: str, status: int):
        self.details = details
        self.status = status


class NotUniqueCityExc(CustomHttpExc):
    def __init__(self, details: str = "Такой город уже добавлен"):
        super().__init__(details, status=409)


class NoSuchCityExc(CustomHttpExc):
    def __init__(
        self, details: str = "Не удалось найти такой город, проверьте данные"
    ):
        super().__init__(details, status=404)


class ForeignServiceExc(CustomHttpExc):
    def __init__(self, details: str = "Ошибка в работе внешнего сервиса"):
        super().__init__(details, status=503)


class MissingParametrExc(CustomHttpExc):
    def __init__(self, field_name: str):
        details = f"Пропущено или не валидно {field_name}"
        super().__init__(details, status=400)