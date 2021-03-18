from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    '''
    print("START")
    print(request.method)
    print(request.headers)
    print(request)
    print(request.data)
    print(request.get_json())
    '''
    rdata = request.get_json()
    if request.method == 'POST':
        return str(int(rdata.get('p1')) * int(rdata.get('p2')) * int(rdata.get('p3')))
    elif request.method == 'GET':
        return render_template('index.html')


'''
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6677, debug=True)
