import os
import uuid
import subprocess
from contextlib import suppress
from flask import Flask
from flask import request
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def debug_request(request):
    print(request)
    # print(request.method)
    # print(request.headers)
    print('files', request.files)
    print('form', request.form)
    print('data', request.data)


def check_input(mat_str):
    l = mat_str.split('\n')
    lines_count = int(l[0])
    assert lines_count == len(l) - 1
    for line in l[1:]:
        # print(lines_count, len(line.split()))
        assert lines_count == len(line.split())
    return True


def process_matrix_mult(data):
    if len(data) != 2:
        raise Exception('Bad data')
    *f, o = map(str, ['/tmp/' + str(uuid.uuid4()) for _ in range(3)])
    for i, filename in enumerate(f):
        with open(filename, 'w') as file:
            file.write(data[i])
    try:
        r = subprocess.run(['./a.out', o, *f], check=True)
        # print('Kernel done')
        # print(r)
        with open(o, 'r') as file:
            return file.read()
    finally:
        with suppress(FileNotFoundError):
            for filename in f + [o]:
                os.remove(filename)


@app.route('/t/', methods=['POST'])
def t():
    debug_request(request)
    return make_response('t ok')


@app.route('/upload/', methods=['POST'])
def upload():
    debug_request(request)
    # check_input(request.form.get('text0'))
    # check_input(request.form.get('text1'))
    
    try:
        result = process_matrix_mult((request.form.get('text0'), request.form.get('text1')))
        return make_response(result)
    except BaseException as e:
        print(type(e), e)
        return make_response(str(e), 500) # 500 Internal Server Error


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6677, debug=True)
