from ninja import ModelSchema

from rpg import models


class QuestReadSchema(ModelSchema):
    class Meta:
        model = models.Quest
        fields = "__all__"
