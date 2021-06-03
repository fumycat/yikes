import os
import re
import uuid
import json
import tempfile
import subprocess
from pathlib import Path
from contextlib import suppress
from flask import Flask
from flask import request
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS

import mgen
import mres

app = Flask(__name__)
CORS(app)

valid_name = re.compile('^[A-Za-z]{1}[A-Za-z0-9]*$')

tmp_folder = Path(os.getcwd()) / 'tmpx' # Path(tempfile._get_default_tempdir())


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
    # TODO more checks (len of in array == functor param len)

    # generate code
    source_name = Path(next(tempfile._get_candidate_names()) + '.cu')
    print('source file', source_name)
    mgen.construct(tmp_folder / source_name, arrays, flow, functors, j.get('t'), j.get('gout'))

    # compile
    executable_name = Path(next(tempfile._get_candidate_names()))
    print('executable file', executable_name)
    try:
        subprocess.run(['nvcc', source_name, '-o', executable_name], check=True, cwd=tmp_folder)
    except subprocess.CalledProcessError as e:
        return make_response(json.dumps({'status': 'Error', 'message': str(e), 'more': 'Compile error'}))
    finally:
        with suppress(FileNotFoundError):
            pass # os.remove(tmp_folder / source_name)

    # execute
    nvprof_log_name = Path(next(tempfile._get_candidate_names()) + '.log')
    print('nvprof file', nvprof_log_name)
    output_name = Path(next(tempfile._get_candidate_names()) + '.txt')
    ea = [output_name] # todo more args for custom containers
    try:
        subprocess.run(['nvprof', '--print-gpu-summary', '--csv', '--log-file', nvprof_log_name, './' + str(executable_name), *ea], check=True, cwd=tmp_folder)
    except subprocess.CalledProcessError as e:
        return make_response(json.dumps({'status': 'Error', 'message': str(e), 'more': 'Execute error'}))
    finally:
        with suppress(FileNotFoundError):
            pass # os.remove(tmp_folder / executable_name)

    
    nvprof_dict = mres.parse_nvprof_log(tmp_folder / nvprof_log_name)
    result_list = mres.parse_output(tmp_folder / output_name, j.get('t'))

    with suppress(FileNotFoundError):
        pass # os.remove(output_name) # nvprof_log_name and more(custom containers)

    response = {'status': 'Ok', 'message': 'Message', 'nvprof': nvprof_dict, 'result': result_list}

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
