from flask import Flask
from flask_restful import Api

from resource import CheckFileCfUpdate, Run1CMerge, CheckIsOnline, SendMessage, CheckUpdate1C, Run1CUpdate, \
    CheckMerge1C

app = Flask(__name__)
api = Api(app)

api.add_resource(CheckFileCfUpdate, '/check_file_cf_update/')

api.add_resource(Run1CMerge, '/run_1c_merge/')
api.add_resource(CheckMerge1C, '/check_merge_1c/')
api.add_resource(Run1CUpdate, '/run_1c_update/')
api.add_resource(CheckUpdate1C, '/check_update_1c/')

api.add_resource(SendMessage, '/send_message/')
api.add_resource(CheckIsOnline, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8383, debug=True)
