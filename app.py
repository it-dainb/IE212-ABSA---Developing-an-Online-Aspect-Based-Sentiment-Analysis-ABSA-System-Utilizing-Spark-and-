from flask import Flask, render_template, request
from flask_cors import CORS
import copy

app = Flask(__name__)
CORS(app)

data = {}
num_cmt = 0

@app.route('/predict', methods=['GET'])
def predict():
    pred = list(data.values())
    pred.sort(key=lambda x: x['num'], reverse=True)
    
    return pred

@app.route('/', methods=['GET', 'POST'])
def home():
    global data, num_cmt
    
    if request.method == 'POST':
        req = request.json
        
        if req['cmtid'] not in data:
            data[req['cmtid']] = {
                "text": req['text'],
                "labels": [],
                'sentiment': req['sentiment'],
                'num': copy.deepcopy(num_cmt)
            }
            num_cmt += 1
        
        data[req['cmtid']]['labels'].append([
            req['begin'],
            req['end'],
            req['label']
        ])
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
