from flask import Flask, render_template, Response, jsonify
import cv2
from utils.detection import ObjectDetector
from utils.webcam import WebcamStream

app = Flask(__name__)
detector = ObjectDetector()
webcam = WebcamStream()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/part_info')
def part_info():
    return jsonify(detector.get_current_part_info())

def generate_frames():
    count = 0
    while True:
        ret, frame = webcam.read()
        if not ret:
            break

        count += 1
        if count % 2 != 0:
            continue

        frame = detector.process_frame(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=False, port=8080)