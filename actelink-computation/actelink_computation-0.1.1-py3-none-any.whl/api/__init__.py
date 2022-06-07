from flask import request
from flask_restx import Api, Resource
import actelink.models as models

api = Api()

@api.route('/_computations/', methods=['POST'])
class Computations(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def post(self):
        data = request.get_json()
        res = models.compute(data)
        if len(res) == 0:
            return [], 400
        return res, 200
