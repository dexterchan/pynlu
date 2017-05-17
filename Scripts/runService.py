'''
Created on May 17, 2017

@author: dexter
'''

#!flask/bin/python
from flask import Flask, jsonify,abort,make_response,request 
from flask import redirect, send_from_directory,Response

from nluModule import  *
from  Models.SentenceModel import Sentence


n = nluModule()

n.loadModel()

app = Flask(__name__)


    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
@app.route('/pib/service/requests', methods=['POST'])
def create_task():
    if not request.json or not 'description' in request.json:
        abort(400)
    
    text = request.json['description']
    
    r=n.findAction(text)
    
    task = {
        'description': text,
        'action': r
    }
    
    #return jsonify({'task': task}), 201
    return Response(json.dumps(task),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,
    host= '0.0.0.0',
    port=int("5000"))