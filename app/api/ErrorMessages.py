from dataclasses import dataclass


@dataclass(frozen=True)
class BaseAPIErrors:
    idErr: str = "{0} с таким id не существует"
    errorOccurred: str = "Произошла ошибка"
    colValLenErr: str = "Кол-во изменяемых колонок и их значений должно быть одинаковым"


@dataclass(frozen=True)
class BrandsAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Бренда")
    nameUsedErr: str = "Бренд с таким названием уже существует"


@dataclass(frozen=True)
class ClientsAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Клиента")


@dataclass(frozen=True)
class PostsAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Должности")


@dataclass(frozen=True)
class ProductAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Товара")


@dataclass(frozen=True)
class StaffAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Сотрудника")


@dataclass(frozen=True)
class TypesOfRepairsAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Вида ремонта")
    nameUsedErr: str = "Такой вид ремонта уже существует"


@dataclass(frozen=True)
class OrdersAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Заказа")


@dataclass(frozen=True)
class ExecutionOfOrdersAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Исполнения")


@dataclass(frozen=True)
class PerformersAPIErrors(BaseAPIErrors):
    idErr: str = BaseAPIErrors.idErr.format("Записи")
