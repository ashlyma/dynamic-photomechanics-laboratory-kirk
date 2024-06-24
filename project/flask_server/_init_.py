from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/list_files', methods=['GET'])
def list_files():
    response = requests.get('http://your-synology-api-url/SYNO.FileStation.List', params={...})
    return jsonify(response.json())

@app.route('/search_files', methods=['GET'])
def search_files():
    query = request.args.get('query')
    response = requests.get('http://your-synology-api-url/SYNO.FileStation.Search', params={'query': query, ...})
    return jsonify(response.json())
