from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/frontend"
    print(root_dir)
    return send_from_directory(root_dir, 'index.html')

@app.route('/search')
def serve_search():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/frontend"
    return send_from_directory(root_dir, 'search.html')

@app.route('/success')
def serve_success():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/frontend"
    return send_from_directory(root_dir, 'success.html')

if __name__ == '__main__':
    app.run(debug=True)