from core.constants import GROUP_ADMINS, GROUP_AGENTS, GROUP_MODERATORS

GROUP_PERMISSION = {
    GROUP_ADMINS: tuple(),
    GROUP_MODERATORS: (
        "change_user",
        "change_team",
        "change_player",
    ),
    GROUP_AGENTS: ("change_player",),
}
