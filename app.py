from flask import Flask, request, redirect, url_for, send_file, render_template
import cv2
import os
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

def blur_watermark(input_video, output_video, x, y, w, h):
    cap = cv2.VideoCapture(input_video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        watermark_area = frame[y:y+h, x:x+w]
        blurred_area = cv2.GaussianBlur(watermark_area, (99, 99), 0)
        frame[y:y+h, x:x+w] = blurred_area
        out.write(frame)

    cap.release()
    out.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_' + file.filename)
        blur_watermark(filepath, output_filepath, 50, 50, 100, 50)  # Adjust coordinates and size as needed
        return send_file(output_filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
