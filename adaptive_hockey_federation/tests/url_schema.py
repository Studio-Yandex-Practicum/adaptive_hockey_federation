PERMISSION_REQUIRED = "permission_required"
URL = "url"

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
ADMIN_LOGOUT = ("/admin/logout/",)
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
# Document был исключен из админки
# ADMIN_DOCUMENT_URL_302 = ("/admin/main/document/<path:object_id>/",)
# ADMIN_DOCUMENT_URLS = (
#     "/admin/main/document/",
#     "/admin/main/document/<path:object_id>/change/",
#     "/admin/main/document/<path:object_id>/delete/",
#     "/admin/main/document/<path:object_id>/history/",
#     "/admin/main/document/add/",
# )
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
# AdminStaffTeamMember был исключен
# ADMIN_STAFF_TEAM_MEMBER_URL_302 = (
#     "/admin/main/staffteammember/<path:object_id>/",
# )
# ADMIN_STAFF_TEAM_MEMBER_URLS = (
#     "/admin/main/staffteammember/",
#     "/admin/main/staffteammember/<path:object_id>/change/",
#     "/admin/main/staffteammember/<path:object_id>/delete/",
#     "/admin/main/staffteammember/<path:object_id>/history/",
#     "/admin/main/staffteammember/add/",
# )
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
    {URL: "/competitions/", PERMISSION_REQUIRED: "list_view_competition"},
    {URL: "/competitions/create/", PERMISSION_REQUIRED: "add_competition"},
    {
        URL: "/competitions/<int:pk>/",
        PERMISSION_REQUIRED: "list_team_competition",
    },
    {
        URL: "/competitions/<int:pk>/edit/",
        PERMISSION_REQUIRED: "change_competition",
    },
)

COMPETITION_POST_URLS = (
    {
        URL: "/competitions/<int:competition_id>/teams/<int:pk>/add/",
        PERMISSION_REQUIRED: "add_team_competition",
    },
    {
        URL: "/competitions/<int:competition_id>/teams/<int:pk>/delete/",
        PERMISSION_REQUIRED: "delete_team_competition",
    },
    {
        URL: "/competitions/<int:pk>/delete/",
        PERMISSION_REQUIRED: "delete_competition",
    },
)

PLAYER_GET_URLS = (
    {URL: "/players/", PERMISSION_REQUIRED: "list_view_player"},
    {URL: "/players/<int:pk>/", PERMISSION_REQUIRED: "view_player"},
    {URL: "/players/<int:pk>/edit/", PERMISSION_REQUIRED: "change_player"},
    {URL: "/players/create/", PERMISSION_REQUIRED: "add_player"},
)
PLAYER_POST_URLS = (
    {URL: "/players/1/delete/", PERMISSION_REQUIRED: "delete_player"},
    # TODO: Тест на данный урл выдает TemplateDoesNotExist. Необходимо
    #   раскомментировать, когда будет починен player_id_deleted() в
    #   main.views или вообще удалить, если эта страница не нужна.
    # "/players/deleted/",
)
STAFF_GET_URLS = (
    {URL: "/staffs/", PERMISSION_REQUIRED: "list_view_staffteammember"},
    {URL: "/staffs/<int:pk>/", PERMISSION_REQUIRED: "view_staffteammember"},
    {
        URL: "/staffs/<int:pk>/edit/",
        PERMISSION_REQUIRED: "change_staffteammember",
    },
    {URL: "/staffs/create/", PERMISSION_REQUIRED: "add_staffteammember"},
)
STAFF_POST_URLS = (
    {
        URL: "/staffs/<int:pk>/delete/",
        PERMISSION_REQUIRED: "delete_staffteammember",
    },
)
TEAM_GET_URLS = (
    {URL: "/teams/", PERMISSION_REQUIRED: "list_view_team"},
    {URL: "/teams/<int:team_id>/", PERMISSION_REQUIRED: "view_team"},
    {URL: "/teams/<int:team_id>/edit/", PERMISSION_REQUIRED: "change_team"},
    {URL: "/teams/create/", PERMISSION_REQUIRED: "add_team"},
)
TEAM_POST_URLS = (
    {URL: "/teams/<int:team_id>/delete/", PERMISSION_REQUIRED: "delete_team"},
)
USER_GET_URLS = (
    {URL: "/users/", PERMISSION_REQUIRED: "list_view_user"},
    {URL: "/users/<int:pk>/edit/", PERMISSION_REQUIRED: "change_user"},
    {URL: "/users/create/", PERMISSION_REQUIRED: "add_user"},
    {
        URL: "/users/set_password/<uidb64>/<token>/",
        PERMISSION_REQUIRED: None,
        "authorized_only": False,
    },
)
USER_POST_URLS = (
    {URL: "/users/<int:pk>/delete/", PERMISSION_REQUIRED: "delete_user"},
)
UNLOAD_URLS = ("/unloads/",)

# Страницы админки, которые должны возвращать 200(ОК) для пользователя,
# обладающего правами администратора:
ADMIN_SITE_ADMIN_OK = (
        (ADMIN_MAIN_URL,)
        + ADMIN_APP_LABELS_URLS
        + ADMIN_AUTH_URLS
        + ADMIN_CITY_URLS
        + ADMIN_COMPETITIONS_URLS
        + ADMIN_DIAGNOSIS_URLS
        + ADMIN_DISCIPLINE_LEVEL_URLS
        + ADMIN_DISCIPLINE_NAME_URLS
        + ADMIN_NOSOLOGY_URLS
        + ADMIN_PASSWORD_URLS
        + ADMIN_PLAYER_URLS
        + ADMIN_PROXY_GROUP_URLS
        + ADMIN_SERVICE_PAGES
        + ADMIN_STAFF_MEMBER_URLS
        + ADMIN_TEAM_URLS
        + ADMIN_USER_URLS
    # + ADMIN_STAFF_TEAM_MEMBER_URLS
    # + ADMIN_DOCUMENT_URLS
)
