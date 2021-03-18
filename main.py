from flask import Flask
from flask import request
from flask import make_response
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6677, debug=False)
