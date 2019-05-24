from flask import Flask, jsonify, request, redirect, url_for
from flask_restful import Resource, Api
from flask_cors import CORS
from sys import stdout
from threading import Thread
from subprocess import Popen
from os import listdir, path, unlink
import wget
import requests
import json
import datetime

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
api = Api(app)
# enable CORS
CORS(app)

scanqueue = []

# TODO:pop id


def scan():
    global scanqueue
    if scanqueue:
        process = Popen("sonar-scanner \
  -Dsonar.projectKey=kururu002_HelpMyBug \
  -Dsonar.organization=kururu002-github \
  -Dsonar.projectBaseDir=/Users/huangpohan/Projects/scan_folder/\
  -Dsonar.sources=/Users/huangpohan/Projects/scan_folder/ \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=fa68b4f253b958b40704e6376201643ba094ff5d", shell=True)
        process.wait()
        scanqueue.pop()
        folder = '/Users/huangpohan/Projects/scan_folder'
        # Clean up
        for the_file in listdir(folder):
            file_path = path.join(folder, the_file)
            try:
                if path.isfile(file_path):
                    unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


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

# TODO: fake data


class List(Resource):
    def get(self):
        ret = {
            'code': 20000, 'data': {
                'items': [{
                    'id': '250337',
                    'title': "Program shutdown immediately after launching for 5 secs",
                    'author': 'kururu002',
                    'status': 'Open',
                    'createdDate': datetime.datetime.now()-datetime.timedelta(minutes=1),
                    'visitorCount': 5
                }]}
        }
        return jsonify(ret)


class Report(Resource):
    #TODO: fill in all
    def post(self):
        global scanqueue
        supportType = ['c', 'cpp', 'h', 'py', 'java', 'xml', 'css', 'js',
                       'abap', 'cls', 'cs', 'php', 'html', 'perl', 'sql', 'ruby']
        my_json = request.data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data['scanRequired']:
            for file in data['fileList']:
                filetype = file['name'].split('.')[-1]
                if filetype in supportType:
                    # TODO: fix download path
                    wget.download(
                        file['url'], '/Users/huangpohan/Projects/scan_folder/')
        # if data.imageRequired:
        #     print('required')
        # if data.scannerRequired:
        #     print('scan')
        scanqueue.append(250337)
        Thread(target=scan).start()
        ret = {'code': 20000, 'data': 'shit'}
        return jsonify(ret)
    def get(self):
        # reportId=request.args.get('reportId')
        global scanqueue
        ret={'code':20000,'data':{'scanCompleted':False}}
        if not scanqueue:
           ret['data']['scanCompleted']=True
        return jsonify(ret)




api.add_resource(User, '/user/login')
api.add_resource(UserInfo, '/user/info')
api.add_resource(List, '/table/list')
api.add_resource(Report, '/report')
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


@app.route('/user/logout', methods=['POST'])
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
