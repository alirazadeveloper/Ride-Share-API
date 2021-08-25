import json


class sentresponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def response(self):
        res = dict()
        res['status'] = self.status
        res['message'] = self.message
        res['data'] = self.data
        return json.loads(json.dumps(res, indent=4))
