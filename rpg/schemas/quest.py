from ninja import ModelSchema

from rpg import models


class QuestReadSchema(ModelSchema):
    class Meta:
        model = models.Quest
        fields = "__all__"


class QuestWriteSchema(ModelSchema):
    title: str

    class Meta:
        model = models.Quest
        fields = "title", "description"

    # resolver used as validator, but with provided context
    # data is dict of provided fields
    @staticmethod
    def resolve_title(data, context):
        print(data)
        title = data.get("title")
        if title == "string":
            raise ValueError("Title cannot be set to 'string'.")

        return title
