from core.constants import Group


class GroupPermission:
    """Разрешения для групп пользователей."""

    GROUP_PERMISSION = {
        Group.ADMINS: (
            "exclude",
            (
                "add_logentry",
                "change_logentry",
                "delete_logentry",
                "view_logentry",
                "add_contenttype",
                "change_contenttype",
                "delete_contenttype",
                "view_contenttype",
                "add_session",
                "change_session",
                "delete_session",
                "view_session",
            ),
        ),
        Group.MODERATORS: (
            "include",
            (
                "change_player",
                "view_player",
                "add_document",
                "change_document",
                "delete_document",
                "view_document",
            ),
        ),
        Group.AGENTS: (
            "include",
            (
                "change_player",
                "view_player",
                "add_player",
                "list_view_player",
                "change_team",
                "view_team",
                "list_view_team",
                "add_document",
                "change_document",
                "delete_document",
                "view_document",
            ),
        ),
    }


REGEX_AREA_CODE_IS_SEVEN_HUNDRED = "^7[0-9]{2,10}$"
