INDEX_PAGE = "/"
ADMIN_MAIN_URL = "/admin/"
ADMIN_APP_LABELS_URLS = (
    "/admin/competitions/",
    "/admin/main/",
    "/admin/users/",
)
ADMIN_AUTH_GROUP_302 = "/admin/auth/group/<path:object_id>/"
ADMIN_AUTH_URLS = (
    "/admin/auth/group/",
    "/admin/auth/group/<path:object_id>/change/",
    "/admin/auth/group/<path:object_id>/delete/",
    "/admin/auth/group/<path:object_id>/history/",
    "/admin/auth/group/add/",
)
ADMIN_COMPETITIONS_URLS_302 = (
    "/admin/competitions/competition/<path:object_id>/",
)
ADMIN_COMPETITIONS_URLS = (
    "/admin/competitions/competition/",
    "/admin/competitions/competition/<path:object_id>/change/",
    "/admin/competitions/competition/<path:object_id>/delete/",
    "/admin/competitions/competition/<path:object_id>/history/",
    "/admin/competitions/competition/add/",
)
ADMIN_SERVICE_PAGES = ("/admin/jsi18n/",)
ADMIN_LOGIN = ("/admin/login/",)
ADMIN_LOGUOT = ("/admin/logout/",)
ADMIN_CITY_URL_302 = ("/admin/main/city/<path:object_id>/",)
ADMIN_CITY_URLS = (
    "/admin/main/city/",
    "/admin/main/city/<path:object_id>/change/",
    "/admin/main/city/<path:object_id>/delete/",
    "/admin/main/city/<path:object_id>/history/",
    "/admin/main/city/add/",
)
ADMIN_DIAGNOSIS_URL_302 = ("/admin/main/diagnosis/<path:object_id>/",)
ADMIN_DIAGNOSIS_URLS = (
    "/admin/main/diagnosis/",
    "/admin/main/diagnosis/<path:object_id>/change/",
    "/admin/main/diagnosis/<path:object_id>/delete/",
    "/admin/main/diagnosis/<path:object_id>/history/",
    "/admin/main/diagnosis/add/",
)
ADMIN_DISCIPLINE_URL_302 = ("/admin/main/discipline/<path:object_id>/",)
ADMIN_DISCIPLINE_URLS = (
    "/admin/main/discipline/",
    "/admin/main/discipline/<path:object_id>/change/",
    "/admin/main/discipline/<path:object_id>/delete/",
    "/admin/main/discipline/<path:object_id>/history/",
    "/admin/main/discipline/add/",
)
ADMIN_DISCIPLINE_LEVEL_URL_302 = (
    "/admin/main/disciplinelevel/<path:object_id>/",
)
ADMIN_DISCIPLINE_LEVEL_URLS = (
    "/admin/main/disciplinelevel/",
    "/admin/main/disciplinelevel/<path:object_id>/change/",
    "/admin/main/disciplinelevel/<path:object_id>/delete/",
    "/admin/main/disciplinelevel/<path:object_id>/history/",
    "/admin/main/disciplinelevel/add/",
)
ADMIN_DISCIPLINE_NAME_URL_302 = (
    "/admin/main/disciplinename/<path:object_id>/",
)
ADMIN_DISCIPLINE_NAME_URLS = (
    "/admin/main/disciplinename/",
    "/admin/main/disciplinename/<path:object_id>/change/",
    "/admin/main/disciplinename/<path:object_id>/delete/",
    "/admin/main/disciplinename/<path:object_id>/history/",
    "/admin/main/disciplinename/add/",
)
ADMIN_DOCUMENT_URL_302 = ("/admin/main/document/<path:object_id>/",)
ADMIN_DOCUMENT_URLS = (
    "/admin/main/document/",
    "/admin/main/document/<path:object_id>/change/",
    "/admin/main/document/<path:object_id>/delete/",
    "/admin/main/document/<path:object_id>/history/",
    "/admin/main/document/add/",
)
ADMIN_NOSOLOGY_URL_302 = ("/admin/main/nosology/<path:object_id>/",)
ADMIN_NOSOLOGY_URLS = (
    "/admin/main/nosology/",
    "/admin/main/nosology/<path:object_id>/change/",
    "/admin/main/nosology/<path:object_id>/delete/",
    "/admin/main/nosology/<path:object_id>/history/",
    "/admin/main/nosology/add/",
)
ADMIN_PLAYER_URL_302 = ("/admin/main/player/<path:object_id>/",)
ADMIN_PLAYER_URLS = (
    "/admin/main/player/",
    "/admin/main/player/<path:object_id>/change/",
    "/admin/main/player/<path:object_id>/delete/",
    "/admin/main/player/<path:object_id>/history/",
    "/admin/main/player/add/",
)
ADMIN_STAFF_MEMBER_URL_302 = ("/admin/main/staffmember/<path:object_id>/",)
ADMIN_STAFF_MEMBER_URLS = (
    "/admin/main/staffmember/",
    "/admin/main/staffmember/<path:object_id>/change/",
    "/admin/main/staffmember/<path:object_id>/delete/",
    "/admin/main/staffmember/<path:object_id>/history/",
    "/admin/main/staffmember/add/",
)
ADMIN_STAFF_TEAM_MEMBER_URL_302 = (
    "/admin/main/staffteammember/<path:object_id>/",
)
ADMIN_STAFF_TEAM_MEMBER_URLS = (
    "/admin/main/staffteammember/",
    "/admin/main/staffteammember/<path:object_id>/change/",
    "/admin/main/staffteammember/<path:object_id>/delete/",
    "/admin/main/staffteammember/<path:object_id>/history/",
    "/admin/main/staffteammember/add/",
)
ADMIN_TEAM_URL_302 = ("/admin/main/team/<path:object_id>/",)
ADMIN_TEAM_URLS = (
    "/admin/main/team/",
    "/admin/main/team/<path:object_id>/change/",
    "/admin/main/team/<path:object_id>/delete/",
    "/admin/main/team/<path:object_id>/history/",
    "/admin/main/team/add/",
)
ADMIN_PASSWORD_URLS = (
    "/admin/password_change/",
    "/admin/password_change/done/",
)
ADMIN_PROXY_GROUP_URL_302 = ("/admin/users/proxygroup/<path:object_id>/",)
ADMIN_PROXY_GROUP_URLS = (
    "/admin/users/proxygroup/",
    "/admin/users/proxygroup/<path:object_id>/change/",
    "/admin/users/proxygroup/<path:object_id>/delete/",
    "/admin/users/proxygroup/<path:object_id>/history/",
    "/admin/users/proxygroup/add/",
)
ADMIN_USER_URL_302 = ("/admin/users/user/<path:object_id>/",)
ADMIN_USER_URLS = (
    "/admin/users/user/",
    "/admin/users/user/<path:object_id>/change/",
    "/admin/users/user/<path:object_id>/delete/",
    "/admin/users/user/<path:object_id>/history/",
    "/admin/users/user/add/",
)
ANALYTICS_URL = "/analytics/"
LOG_IN_URL = "/auth/login/"
LOG_OUT_URL = "/auth/logout/"
PASSWORD_URLS = (
    "/auth/password_change/",
    "/auth/password_change/done/",
    "/auth/password_reset/",
    "/auth/password_reset/done/",
)
AUTH_RESET_URLS = (
    "/auth/reset/<uidb64>/<token>/",
    "/auth/reset/done/",
)
COMPETITION_GET_URLS = (
    "/competitions/",
    "/competitions/create/",
    "/competitions/<int:pk>/",
    "/competitions/<int:pk>/edit/",
)
COMPETITION_POST_URLS = (
    "/competitions/<int:competition_id>/teams/<int:pk>/add/",
    "/competitions/<int:competition_id>/teams/<int:pk>/delete/",
    "/competitions/<int:pk>/delete/",
)
PLAYER_GET_URLS = (
    "/players/",
    "/players/<int:pk>/",
    "/players/<int:pk>/edit/",
    "/players/create/",
)
PLAYER_POST_URLS = (
    "/players/1/delete/",
    # TODO: Тест на данный урл выдает TemplateDoesNotExist. Необходимо
    #  раскомментировать, когда будет починен player_id_deleted() в
    #  main.views или вообще удалить, если эта страница не нужна.
    # "/players/deleted/",
)
STAFF_GET_URLS = (
    "/staffs/",
    "/staffs/<int:pk>/",
    "/staffs/<int:pk>/edit/",
    "/staffs/create/",
)
STAFF_POST_URL = ("/staffs/<int:pk>/delete/",)
TEAM_GET_URLS = (
    "/teams/",
    "/teams/<int:team_id>/",
    "/teams/<int:team_id>/edit/",
    "/teams/create/",
)
TEAM_POST_URL = "/teams/<int:team_id>/delete/"
USER_GET_URLS = (
    "/users/",
    "/users/<int:pk>/edit/",
    "/users/create/",
    "/users/set_password/<uidb64>/<token>/",
)
USER_POST_URL = "/users/<int:pk>/delete/"
UNLOAD_URLS = ("/unloads/",)
