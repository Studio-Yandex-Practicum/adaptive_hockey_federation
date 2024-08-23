from typing import Any

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from games.constants import GAME_TITLE_MAPPING, Literals
from games.models import Game


class GameCreateUpdateMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Миксин для представлений создания и редактирования игры."""

    model = Game
    success_url = reverse_lazy("games:games")
    template_name = "main/games/game_create_edit.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Метод для получения словаря context в шаблоне страницы."""
        context = super(GameCreateUpdateMixin, self).get_context_data(**kwargs)
        return dict(
            **context,
            page_title=GAME_TITLE_MAPPING[type(self).__name__],
            help_text_role=Literals.GAME_CHOSEN_TEAMS,
        )

    # def get_success_url(self) -> str:
    #     """
    #     Метод для получения URL-адреса для перенаправления по
    #     успешному заполнению формы.
    #     """
    #     return reverse(
    #         "games:game_id", kwargs={"pk": self.object.pk}
    #     )
    # TODO: раскомментировать, когда появится контроллер для просмотра
    #  игры (! future update)
