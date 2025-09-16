import os
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/detect", methods=["POST"])
def detect():
    # Check if audio file was uploaded
    if "audio.wav" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio.wav"]

    # Create a safe, timestamped filename to avoid overwriting
    base_name = audio_file.filename or "audio.wav"
    safe_name = secure_filename(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    fname = f"{timestamp}_{safe_name}"
    save_path = os.path.join(UPLOAD_FOLDER, fname)

    # Save the file
    audio_file.save(save_path)

    print(f"Saved audio file to: {save_path}")

    # Dummy response (replace with real detection later)
    return jsonify({
        "status": "success",
        "saved_path": save_path,
        "deepfake_detected": False,
        "confidence": 0.05
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
