import os
import subprocess
from flask import Flask
from flask import request
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/t/', methods=['POST'])
def t():
    print(request)
    print(request.method)
    print(request.headers)
    print('files', request.files)
    print('form', request.form)
    print('data', request.data)
    return make_response('t ok')

@app.route('/upload/', methods=['POST'])
def upload():
    
    print(request)
    print(request.method)
    print(request.headers)
    print('files', request.files)
    print('form', request.form)
    print('data', request.data)
    
    with open('file0.txt', 'w') as f:
        f.write(request.form.get('text0'))
    
    with open('file1.txt', 'w') as f:
        f.write(request.form.get('text1'))

    print("Got files")
    r = subprocess.run(["./a.out", "file0.txt", "file1.txt"])
    print(r)
    if r.returncode == 0:
        with open('out.txt', 'r') as f:
            return make_response(f.read())
    else:
        return make_response('error', 500) # 500 Internal Server Error

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6677, debug=True)
