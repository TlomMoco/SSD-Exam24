import io

from flask import Blueprint, request, jsonify, session, flash, send_file, redirect, url_for
import os
from functools import wraps
from werkzeug.utils import secure_filename
from EducationalSystem.app import config
from EducationalSystem.app.models import user_model
from EducationalSystem.app.models import file_model


file_controller = Blueprint("file_controller", __name__)


# Decorator to require API key for secure file uploads and access control
def user_token_required(f):
    @wraps(f) # This ensures that the original function name is retained
    def decorator_function(*args, **kwargs):
        user_token = session.get("user_token")
        user = user_model.find_user_token(user_token)
        if not user and not user_token:
            return jsonify({"message": "Invalid user or user_token"}), 401
        if user[4] != "teacher" and request.endpoint == "file_controller.upload":
            return jsonify({"message": "You are not allowed to upload file"}), 403
        return f(*args, **kwargs)
    return decorator_function


# Route for uploading file, restricted to teachers only
@file_controller.route("/upload", methods=["GET", "POST"])
@user_token_required
def upload_file():
    if request.method == "POST":
        role = session.get("role")
        if role != "teacher":
            return jsonify({"message": "Unauthorized: Only teachers can upload files"}), 400

        if "file" not in request.files:
            return jsonify({"message": "No file"}), 400

        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            content = file.read()
            uploader_id = session.get("user_id")
            # Saving file to the uploads directory
            file.save(os.path.join(config.Config.UPLOAD_FOLDER, filename))

            if not uploader_id:
                return jsonify({"message": "No user logged in"}), 400

            # Storing file in the database
            file_model.save_file_metadata(filename, uploader_id, content)
            flash("File Uploaded", "success")
            jsonify({"message": "File uploaded"}), 200
            return redirect(url_for("auth_bp.dashboard"))
        flash(f"Upload failed - allowed files: {config.Config.ALLOWED_EXTENSIONS}", "error")
        jsonify({"message": "Invalid File"}), 400
        return redirect(url_for("auth_bp.dashboard"))


# Route for downloading files
@file_controller.route("/download/<filename>", methods=["GET"])
@user_token_required
def download_file(filename):
    file_data = file_model.get_file_content(filename)
    print(f"file_data: {file_data}")
    if file_data:
        file_stream = io.BytesIO(file_data)
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    else:
        flash("File not found", "error")
        return redirect(url_for("auth_bp.dashboard"))

# Helper function to check allowed extensions in the config file
def allowed_file(filename):
    return "." in filename and os.path.splitext(filename)[1] in config.Config.ALLOWED_EXTENSIONS

