import os

class Config:
    # Secret key used for session management - if not set a default value is provided
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_key_for_this_educational_system"
    UPLOAD_FOLDER = os.environ.get(os.getcwd(), "uploads")

    # Files allowed to upload (resembling exam files)
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


