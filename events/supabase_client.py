# events/supabase_client.py
from supabase import create_client
from django.conf import settings

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

def upload_file(file, filename):
    response = supabase.storage.from_("calendar-files").upload(
        path=filename,
        file=file.read(),
        file_options={"content-type": file.content_type}
    )
    
    # Get public URL
    public_url = supabase.storage.from_("calendar-files").get_public_url(filename)
    
    return public_url