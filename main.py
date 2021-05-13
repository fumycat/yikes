import os
from flask import Flask
from flask import request
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/ajax/', methods=['POST'])
def ajax_sum():
    '''
    print(request)
    print(request.method)
    print(request.headers)
    print(request.data)
    print(request.get_json())
    '''
    rdata = request.get_json()
    print(rdata)
    return make_response(str(int(rdata.get('p1')) + int(rdata.get('p2')) + int(rdata.get('p3'))))

@app.route('/upload/', methods=['POST'])
def upload():
    '''
    print(request)
    print(request.method)
    print(request.headers)
    print(request.files)
    print(request.form)
    print('data', request.data)
    '''
    with open('file0.txt', 'w') as f:
        f.write(request.form.get('text0'))
    
    with open('file1.txt', 'w') as f:
        f.write(request.form.get('text1'))

    return make_response('ok')
    # if 'file' not in request.files:
    #     print('No file part')
    #     return make_response('no file')
    # file = request.files['file']
    # if file.filename == '':
    #     print('No selected file')
    #     return make_response('No selected file')
    # if file:
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join('', filename))
    #     return make_response('ok')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6677, debug=True)
