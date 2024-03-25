from core.utils import generate_file_name, is_uploaded_file_valid
from main.models import Document


class FileUploadMixin:

    @staticmethod
    def add_new_documents(player, new_files_names, new_files_paths):
        for name, file in zip(new_files_names, new_files_paths):
            if is_uploaded_file_valid(file):
                file.name = generate_file_name(file.name, str(player.id))
                Document.objects.create(player=player, file=file, name=name)

    @staticmethod
    def delete_documents(player, deleted_files_paths):
        for doc in player.player_documemts.all():
            if doc.file.url in deleted_files_paths:
                doc.delete()
