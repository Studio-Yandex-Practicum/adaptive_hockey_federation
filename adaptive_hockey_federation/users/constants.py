from core.constants import GROUP_ADMINS, GROUP_AGENTS, GROUP_MODERATORS

GROUP_PERMISSION = {
    GROUP_ADMINS: (
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
    GROUP_MODERATORS: (
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
    GROUP_AGENTS: (
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
