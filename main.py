import os
import re
import uuid
import json
import subprocess
from contextlib import suppress
from flask import Flask
from flask import request
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

valid_name = re.compile('^[A-Za-z]{1}[A-Za-z0-9]*$')

# nvprof --print-gpu-summary --csv --log-file {log.txt} {./a.out} {params}

def debug_request(request):
    print(request)
    # print(request.method)
    # print(request.headers)
    print('files', request.files)
    print('form', request.form)
    print('data', request.data)


@app.route('/t/', methods=['POST'])
def t():
    # debug_request(request)
    print('.\ngot /t [POST] request')
    j = json.loads(request.data.decode())
    
    from pprint import pprint
    pprint(j)

    arrays = j.get('arrays')
    functors = j.get('functors')
    flow = j.get('flow')

    #print('arrays', arrays)
    #print('functors', functors)
    #print('flow', flow)

    # check input
    if any(not valid_name.match(arr['name']) for arr in arrays):
        return make_response('bad array name', 500)
    # TODO more checks

    response = {'status': 'Ok', 'message': 'Message'}

    return make_response(json.dumps(response))

# DEL THIS
'''
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


@app.route('/upload/', methods=['POST'])
def upload():
    debug_request(request)
    
    try:
        result = process_matrix_mult((request.form.get('text0'), request.form.get('text1')))
        return make_response(result)
    except BaseException as e:
        print(type(e), e)
        return make_response(str(e), 500) # 500 Internal Server Error
'''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6677, debug=True)
