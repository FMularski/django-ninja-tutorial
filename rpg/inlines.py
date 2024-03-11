from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from rpg import models


class ItemInline(admin.TabularInline):
    model = models.Item
    fields = "name", "rarity", "icon_", "icon", "boosted_stat", "value"
    readonly_fields = ("icon_",)
    extra = 1

    def icon_(self, obj):
        style = f"""
            width: 64px;
            height: 64px;
            border-radius: 10px;
            box-shadow: 0px 0px 5px 5px {obj.rarity.color};
        """
        icon_html = f"""
            <img src="{settings.MEDIA_URL}{obj.icon.name}" style="{style}" />
        """
        return format_html(icon_html)


class CharacterInline(admin.StackedInline):
    model = models.Character
    fields = (
        "name",
        "character_class",
        "level",
    )
    readonly_fields = fields
    extra = 0
    can_delete = False
    max_num = 0
    ordering = ("name",)
