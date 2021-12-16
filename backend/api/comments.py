from flask_restx import Namespace, Resource
from .comment_model import comment_model

api = Namespace("comments", description="All comment operations")

COMMENTS_MOCK = [
    {
        "comment": "Explanation\nWhy the edits made under my username Hardcore Metallica Fan were reverted? They weren't vandalisms, just closure on some GAs after I voted at New York Dolls FAC. And please don't remove the template from the talk page since I'm retired now.89.205.38.27",
        "position": {"x": -3.3748245, "y": -0.37758058},
        "classification": {
            "toxic": False,
            "severeToxic": False,
            "obscene": False,
            "threat": False,
            "insult": False,
            "identityHate": False,
        },
    }
]


@api.route("/")
class CommentResource(Resource):
    @api.doc("List comments")
    @api.marshal_list_with(comment_model)
    def get(self):
        return COMMENTS_MOCK

    @api.doc("Classify comment")
    @api.expect(comment_model)
    @api.marshal_with(comment_model, code=201)
    def post(self):
        return COMMENTS_MOCK[0], 201
