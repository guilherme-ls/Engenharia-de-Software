from flask import Flask, send_from_directory, jsonify, request
import os
import json
import random

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

@app.route('/incorrect')
def serve_incorrect():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/frontend"
    return send_from_directory(root_dir, 'incorrect.html')

@app.route('/hint')
def serve_hint():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/frontend"
    return send_from_directory(root_dir, 'hint.html')

@app.route('/api/random_tree')
def api_random_tree():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trees.json")
    with open(db_path, encoding="utf-8") as f:
        trees = json.load(f)
    tree = random.choice(trees)
    return jsonify(tree)

@app.route('/api/tree_by_number/<int:number>')
def api_tree_by_number(number):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trees.json")
    with open(db_path, encoding="utf-8") as f:
        trees = json.load(f)
    for tree in trees:
        if tree["number"] == number:
            return jsonify(tree)
    return jsonify({"error": "Tree not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)