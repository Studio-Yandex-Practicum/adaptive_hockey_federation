from django.contrib.auth.mixins import AccessMixin


class AdminRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_moderator or request.user.is_agent:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
