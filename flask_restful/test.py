from flask import Flask, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'about':'Hello World!'}

    def post(self):
        if not request.json:
            return "{ 'err' : 'json format' }"
        jsoned = request.get_json()
        return ({'you-send': jsoned }), 201 #jsonify

class Multi(Resource):
    def get(self, num):
        return {'result': num*10}

api.add_resource(HelloWorld, '/abc')
api.add_resource(Multi, '/multi/<int:num>')

@app.route('/', methods=['GET', 'POST'])
def index():
    return "test"

if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
