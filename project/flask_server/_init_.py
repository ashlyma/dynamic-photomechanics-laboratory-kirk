from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace these variables with your actual NAS details
NAS_IP = '10.10.52.142'
PORT = '5000'  # Default port for DSM web access
USERNAME = 'AshlyMR'  # Replace with your username
PASSWORD = 'Mylopecru@434343'  # Replace with your password

# Function to authenticate and get the session ID (sid)
def get_session_id():
    login_url = f'http://{NAS_IP}:{PORT}/webapi/auth.cgi'
    login_payload = {
        'api': 'SYNO.API.Auth',
        'version': '3',
        'method': 'login',
        'account': USERNAME,
        'passwd': PASSWORD,
        'session': 'FileStation',
        'format': 'sid'
    }
    try:
        login_response = requests.get(login_url, params=login_payload, timeout=10)  # Set timeout to 10 seconds
        login_data = login_response.json()
        
        if login_data['success']:
            return login_data['data']['sid']
        else:
            raise Exception('Authentication failed.')
    except requests.exceptions.Timeout:
        raise Exception('Connection to Synology NAS timed out.')
    except requests.exceptions.RequestException as e:
        raise Exception(f'Error connecting to Synology NAS: {e}')
    
@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/list_files', methods=['GET'])
def list_files():
    try:
        sid = get_session_id()
        target_folder = request.args.get('/volume1/DPML Shared Folder/Demo Project')  # Replace with your target folder path
        list_url = f'http://{NAS_IP}:{PORT}/webapi/entry.cgi'
        list_payload = {
            'api': 'SYNO.FileStation.List',
            'version': '2',
            'method': 'list',
            'folder_path': target_folder,
            '_sid': sid
        }
        response = requests.get(list_url, params=list_payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/search_files', methods=['GET'])
def search_files():
    try:
        sid = get_session_id()
        query = request.args.get('query')
        search_url = f'http://{NAS_IP}:{PORT}/webapi/entry.cgi'
        search_payload = {
            'api': 'SYNO.FileStation.Search',
            'version': '2',
            'method': 'start',
            'folder_path': '/your_default_folder',  # Replace with your target folder path
            'pattern': query,
            '_sid': sid
        }
        response = requests.get(search_url, params=search_payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/create_directory', methods=['POST'])
def create_directory():
    try:
        app.logger.info("Received request to create directory")
        sid = get_session_id()
        app.logger.info(f"Obtained session ID: {sid}")
        target_folder = request.json.get('target_folder')
        app.logger.info(f"Target folder: {target_folder}")
        create_url = f'http://{NAS_IP}:{PORT}/webapi/entry.cgi'
        create_payload = {
            'api': 'SYNO.FileStation.CreateFolder',
            'version': '2',
            'method': 'create',
            'folder_path': '/volume1/DPML Shared Folder',
            'name': 'directory_name',  # Adding a name parameter
            '_sid': sid
        }
        response = requests.post(create_url, data=create_payload)
        
        # Log the response from Synology API
        app.logger.info(f"Response from Synology API: {response.json()}")
        
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error in create_directory: {e}")
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)