from flask_restx import Resource, abort
from .dataset_api import data_point_model
from ...model.model import model
from ...model.dimension_reduction_loader import reduction_models_loader
from ...flask_setup.flask import app
from ..models.classification_models import classification_api, classification_input
from .dataset_api import validate_input
from ...data.data_loader import data_loader


@classification_api.route("/")
class ClassificationResource(Resource):
    @classification_api.doc(
        description=f"Classify given samples\n\ndatasetName one from:{data_loader.get_dataset_names()}\n\navailableReductionModel: Name of the algorithm from /datasets endpoint which was used to reduce data dimension.\n\textSamples:list of phrases to classify"
    )
    @classification_api.expect(classification_input)
    @classification_api.marshal_list_with(data_point_model)
    def post(self):
        input_json = classification_api.payload
        text_samples: list[str] = input_json["textSamples"]
        algorithm: str = input_json["availableReductionModel"]
        dataset_name: str = input_json["datasetName"]
        if len(text_samples) == 0:
            abort(
                400,
                "An empty list was provided. Please send text to classify",
            )
        validate_input(dataset_name, algorithm)
        try:
            (last_layer_outputs, predictions) = model.predict(text_samples)
            reduction_model = reduction_models_loader.get_model(dataset_name, algorithm)
            response_classification_fields = [
                "toxic",
                "severeToxic",
                "obscene",
                "threat",
                "insult",
                "identityHate",
            ]
            label_list = app.config["LABEL_LIST"]
            response = []
            for i, text_sample in enumerate(text_samples):
                position = reduction_model.transform(last_layer_outputs)
                sample_record = {
                    "text": text_sample,
                    "position": {"x": position[i][0], "y": position[i][1]},
                    "classification": {},
                }
                for index, class_label in enumerate(label_list):
                    sample_record["classification"][
                        response_classification_fields[index]
                    ] = {
                        "assigned": bool(round(predictions[i][class_label])),
                        "prediction": round(predictions[i][class_label] * 100, 2),
                    }
                response.append(sample_record)
            return response, 200
        except:
            abort(500, "Model Inference Failed")
