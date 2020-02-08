from flask_restful import Resource
from dashmachine.version import version


class GetVersion(Resource):
    def get(self):
        return {"Version": version}
