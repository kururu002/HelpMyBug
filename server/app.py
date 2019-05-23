from flask import Flask, jsonify, request, redirect, url_for
from flask_restful import Resource,Api
from flask_cors import CORS
from sys import stdout
import requests
import json
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
api=Api(app)
# enable CORS
CORS(app)
class User(Resource):
    def post(self):
        ret = {'code': 20000, 'data': {'token': 'user-token'}}
        return jsonify(ret) 
class UserInfo(Resource):
    def get(self):
        ret = {
        'code': 20000, 'data': {
            'roles': ['editor'],
            'introduction': 'I am an editor',
            'avatar':
            'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Normal Editor'}}
        return jsonify(ret)
api.add_resource(User,'/user/login')
api.add_resource(UserInfo,'/user/info')
# @app.route('/user/login', methods=['GET', 'PUT', 'OPTIONS', 'POST'])
# def getUser():
#     ret = {'code': 20000, 'data': {'token': 'user-token'}}
#     return jsonify(ret)


# @app.route('/user/info')
# def getUserInfo():
#     ret = {
#         'code': 20000, 'data': {
#             'roles': ['editor'],
#             'introduction': 'I am an editor',
#             'avatar':
#             'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
#             'name': 'Normal Editor'}}
#     return jsonify(ret)


@app.route('/user/logout',methods=['POST'])
def logout():
    ret = {'code': 20000, 'data': 'success'}
    return jsonify(ret)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')



@app.route('/auth/<provider>', methods=['OPTIONS', 'POST'])
def login(provider):
    if request.method == 'OPTIONS':
        return jsonify('shit')
    headers = {'Accept': 'application/json'}
    post_data = json.loads(request.data)
    post_data['client_secret'] = "4f65f9b418a36c9e62221ea91a2f5d54d1667174"
    if post_data['redirectUri']:
        del post_data['redirectUri']
    if post_data['clientId']:
        post_data['client_id'] = post_data['clientId']
        del post_data['clientId']
    response = requests.post(
        'https://github.com/login/oauth/access_token', headers=headers, params=post_data)
    json_data = response.json()
    return jsonify(json_data)


if __name__ == '__main__':
    app.run(debug=True)
