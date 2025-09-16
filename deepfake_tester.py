import io
import wave
import time
import threading
import requests
import pyaudio

# Audio capture setup
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 4
API_URL = "http://localhost:5000/detect"  # change if your server is elsewhere

p = pyaudio.PyAudio()

# (Optional) choose a specific input device index if needed:
# print available devices to check indices:
def list_devices():
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(i, info.get("name"), info.get("maxInputChannels"))

# Uncomment the next line if you want to print devices for debugging:
# list_devices()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                # If you get overflow errors, set exception_on_overflow=False in read()
                )

def capture_audio():
    try:
        while True:
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                except Exception as e:
                    # handle device hiccups gracefully
                    print("Read error (continuing):", e)
                    continue
                frames.append(data)

            # Join raw frames and write a proper WAV file into memory
            audio_data = b"".join(frames)
            buf = io.BytesIO()
            wf = wave.open(buf, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_data)
            wf.close()
            buf.seek(0)

            # Send to deepfake detection API as a proper file-like object
            files = {"audio.wav": ("audio.wav", buf, "audio/wav")}
            try:
                resp = requests.post(API_URL, files=files, timeout=10)
                print("Server response:", resp.status_code, resp.text)
            except requests.exceptions.RequestException as e:
                print("Request failed:", e)

            # small pause so loop doesn't spin too tight
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Capture stopped by user")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    t = threading.Thread(target=capture_audio, daemon=True)
    t.start()
    print("Capturing audio in background. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")
