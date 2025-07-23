from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__, static_folder='website')

# Directory where recorded images are stored
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opencv', 'recorded_images')
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opencv', 'measurements.csv')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

@app.route('/latest_measurement')
def latest_measurement():
    try:
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            latest = df.iloc[-1].to_dict()
            return jsonify(latest)
        else:
            return jsonify(None)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
