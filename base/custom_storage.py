from django.core.files.storage import Storage
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

    def _open(self, name, mode='rb'):
        # This method should return a file-like object, but for a Supabase storage backend, you don't typically need to open files.
        # You can return None or raise NotImplementedError if you don't need to support opening files.
        return None

    def _save(self, name, content):
        file_data = content.read()

        try:
            self.supabase.storage.from_("files").upload(
                path=name,
                file=file_data,
            )
        except Exception as e:
            raise Exception(f"Supabase upload failed: {e}")

        return name

    def url(self, name):
        return self.supabase.storage.from_('files').get_public_url(name)
    
    def exists(self, name):
        try:
            res = self.supabase.storage.from_('files').list(path=os.path.dirname(name))
            return any(file['name'] == os.path.basename(name) for file in res)
        except Exception as e:
            print(f"Error checking if file exists: {str(e)}")
            return False