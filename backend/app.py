from modules.flask_setup.flask import app
from modules.api.setup import api

# initialize restx api
api.init_app(app)

# initialize model
if __name__ == "__main__":
    app.run(app.config["HOST"], port=app.config["PORT"])
