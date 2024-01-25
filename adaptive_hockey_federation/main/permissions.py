from django.contrib.auth.mixins import UserPassesTestMixin


class AdminOnly(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'admin'
        )
