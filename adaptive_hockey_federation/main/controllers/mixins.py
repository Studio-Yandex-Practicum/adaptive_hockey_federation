from main.models import Diagnosis


class DiagnosisListMixin:
    """Миксин для использования в видах редактирования и создания команд."""

    @staticmethod
    def get_diagnosis():
        """Возвращает список диагнозов из БД."""
        return Diagnosis.objects.values_list("name", flat=True)
