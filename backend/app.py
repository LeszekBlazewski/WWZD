from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
api = Api(app)

# load config
if os.getenv("ENV") == "development":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")


@api.route("/api/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


if __name__ == "__main__":
    app.run(app.config["HOST"], port=app.config["PORT"])
