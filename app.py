from flask import Flask, request, jsonify
import os
import time
from datetime import datetime, timedelta
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Flexible storage path (works on any computer)
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "student_images")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cleanup function to delete old images
def cleanup_old_images():
    """Deletes images older than 24 hours."""
    print("Checking for old images...")

    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Only delete files older than 24 hours
        if os.path.isfile(filepath) and now - os.path.getmtime(filepath) > 86400:  # 86400 seconds = 24 hours
            os.remove(filepath)
            print(f"Deleted: {filepath}")

# Run cleanup when Flask app starts
cleanup_old_images()

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    filename = f"student_{int(time.time())}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save the file
    file.save(filepath)
    print(f"Image saved at: {filepath}")

    return jsonify({"status": "success", "path": filepath})

if __name__ == '__main__':
    app.run(debug=True)
