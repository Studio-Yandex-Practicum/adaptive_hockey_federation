from core.utils import generate_file_name, is_uploaded_file_valid
from main.models import Document


class FileUploadMixin:
    """Класс-миксин для загрузки файлов."""

    @staticmethod
    def add_new_documents(player, new_files_names, new_files_paths):
        """Метод для добавления документов."""
        for name, file in zip(new_files_names, new_files_paths, strict=False):
            if is_uploaded_file_valid(file):
                file.name = generate_file_name(
                    file.name,
                    str(player.id) + "-" + name,
                )
                Document.objects.create(player=player, file=file, name=name)

    @staticmethod
    def delete_documents(player, deleted_files_paths):
        """Метод для удаления документов."""
        for doc in player.player_documemts.all():
            if doc.file.url in deleted_files_paths:
                doc.delete()
