from sqladmin import ModelView

from src.database.models import User


# визначаємо зміст адмін-панелі: якими моделями бази даних і якими полями хочемо керувати через адмін-панель:
class UserAdmin(ModelView, model=User):
    column_list = [User.username, User.email, User.phone, User.user_role, User.confirmed, User.created_at, User.updated_at]
    column_searchable_list = [User.username]
    column_sortable_list = [User.user_id, User.user_role]
    column_default_sort = [(User.email, True), (User.username, False)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    name = "Користувач"
    name_plural = "Користувачі"
    icon = "fa-solid fa-user"

