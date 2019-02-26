import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from google.appengine.ext import ndb

app = Flask(__name__)
'''
todos = [{
          "id": 1555555,
          "text":"learn git"
         },
         {
           "id": 1555555,
           "text":"practise python"
         }
      ] '''
'''
container = ['Hello World!', 'Google']

@app.route('/mainpage/')
def mainpage():
    return jsonify(container)

@app.route('/get/<number>')
def get(number):
    if int(number) > len(container):
        return 'That number is greater than the size of the container'
    else:
        return jsonify(container[int(number)])

@app.route('/post/<word>')
def post(word):
    container.append(word)
    return jsonify(word)

@app.route('/delete/<number>')
def delete(number):
    if int(number) > len(container):
        return 'That number is greater than the size of the container'
    else:
        container.pop(int(number))
        return 'Success'''


class requirement(ndb.Model):
    comments = ndb.StringProperty(indexed=False)


@app.route('/')
def main():
    return render_template('form.html')


@app.route('/GET/v1/todos', methods=['GET'])
def mainpage():
    temp_dict = []
    result = requirement.query().fetch()
    for item in result:
        temp_dict.append({'id': item.key.id(), 'data': item.comments})
    return jsonify({"todos": temp_dict, "success": True})


@app.route('/POST/v1/todos', methods=['POST'])
def save():
    comment = request.json['data']
    requirements = requirement()
    requirements.comments = comment
    requirements.put()
    return jsonify({"data": requirements.comments})


@app.route('/PUT/v1/todos/<int:number>', methods=['PUT'])
def put(number):
    key = ndb.Key('requirement', number)
    element = key.get()
    element.comments = request.json['data']
    element.put()
    return jsonify({"success": True})


@app.route('/delete/<int:number>', methods=['DELETE'])
def delete(number):
    key = ndb.Key('requirement', number)
    key.delete()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
