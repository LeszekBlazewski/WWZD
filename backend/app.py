from modules.flask_setup.flask import app
from modules.api.setup import blueprint

# initialize restx api
app.register_blueprint(blueprint)

# initialize model
if __name__ == "__main__":
    app.run(app.config["HOST"], port=app.config["PORT"])
