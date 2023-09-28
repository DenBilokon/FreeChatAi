from sqladmin import ModelView

from src.database.models import User, City, Country, SubscribePlan, MasterInfo, Service, ServiceCategories, UserResponse


# визначаємо зміст адмін-панелі: якими моделями бази даних і якими полями хочемо керувати через адмін-панель:
class UserAdmin(ModelView, model=User):
    column_list = [User.name, User.email, User.phone, User.user_role, User.country_id, User.city_id, User.confirmed, User.created_at, User.updated_at]
    column_searchable_list = [User.name]
    column_sortable_list = [User.user_id, User.user_role, User.country_id, User.city_id]
    column_default_sort = [(User.email, True), (User.name, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Користувач"
    name_plural = "Користувачі"
    icon = "fa-solid fa-user"


class MasterInfoAdmin(ModelView, model=MasterInfo):
    column_list = "__all__"
    column_searchable_list = [MasterInfo.master_id]
    column_sortable_list = [MasterInfo.plan_id]
    column_default_sort = [(MasterInfo.plan_id, True), (MasterInfo.user_id, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Майстер"
    name_plural = "Майстри"
    icon = "fa-solid fa-user-gear"


class CityAdmin(ModelView, model=City):
    column_list = "__all__"
    column_searchable_list = [City.city_ukr]
    column_sortable_list = [City.city_id]
    column_default_sort = [(City.city_id, True), (City.city_ukr, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Місто"
    name_plural = "Міста"
    icon = "fa-solid fa-city"


class SubscribePlanAdmin(ModelView, model=SubscribePlan):
    column_list = "__all__"
    column_searchable_list = [SubscribePlan.subscribe_plan]
    column_sortable_list = [SubscribePlan.plan_id]
    column_default_sort = [(SubscribePlan.subscribe_plan, True), (SubscribePlan.plan_id, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "План підписки"
    name_plural = "Плани підписки"
    icon = "fa-solid fa-file-invoice-dollar"


class CountryAdmin(ModelView, model=Country):
    column_list = "__all__"
    column_searchable_list = [Country.country_ukr]
    column_sortable_list = [Country.country_id]
    column_default_sort = [(Country.country_id, True), (Country.country_ukr, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Країна"
    name_plural = "Країни"
    icon = "fa-solid fa-earth-americas"


class ServiceCategoryAdmin(ModelView, model=ServiceCategories):
    column_list = "__all__"
    column_searchable_list = [ServiceCategories.service_category_ua, ServiceCategories.service_category_en]
    column_sortable_list = [ServiceCategories.service_category_ua, ServiceCategories.service_category_en]
    column_default_sort = [(ServiceCategories.service_category_ua, True), (ServiceCategories.service_category_en, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Група послуг"
    name_plural = "Групи послуг"
    icon = "fa-solid fa-users-gear"


class ServiceAdmin(ModelView, model=Service):
    column_list = "__all__"
    column_searchable_list = [Service.service_ua, Service.service_en]
    column_sortable_list = [Service.service_ua, Service.service_en]
    column_default_sort = [(Service.service_ua, True), (Service.service_en, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Послуга"
    name_plural = "Послуги"
    icon = "fa-solid fa-scissors"


class UserResponseAdmin(ModelView, model=UserResponse):
    column_list = "__all__"
    column_searchable_list = [UserResponse.rate, UserResponse.master_id]
    column_sortable_list = [UserResponse.rate, UserResponse.updated_at]
    column_default_sort = [(UserResponse.updated_at, True), (UserResponse.user_id, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Відгук"
    name_plural = "Відгуки"
    icon = "fa-regular fa-comment"