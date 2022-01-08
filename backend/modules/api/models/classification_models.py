from flask_restx import Namespace, fields
from ...data.dataset_loader import dataset_loader

classification_api = Namespace(
    "classification", description="Operations regarding classification of new samples"
)

classification_input = classification_api.model(
    "ClassificationInput",
    {
        "datasetName": fields.String(
            required=True,
            description=f"Name of dataset from: {dataset_loader.get_dataset_names()} for which reduction model will be loaded",
        ),
        "availableReductionModel": fields.String(
            required=True,
            description="Name of the algorithm from /datasets endpoint which was used to reduce data dimension",
        ),
        "textSamples": fields.List(
            fields.String,
            required=True,
            description="List of phrases (strings) to be analyzed for toxicity.",
        ),
    },
)
