from flask import jsonify


class ApiError(Exception):
    def __init__(self, message, payload=None, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload or ()
        # loggin etc.

    def get_response(self):
        ret = dict(self.payload)
        ret['message'] = self.message
        return jsonify(ret), self.status_code
