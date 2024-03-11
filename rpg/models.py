from colorfield.fields import ColorField
from django.db import models


class Guild(models.Model):
    name = models.CharField(max_length=100)
    banner = models.ImageField(upload_to="banners/")

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Statistics(models.Model):
    base_health = models.IntegerField(default=100)
    base_max_health = models.IntegerField(default=100)
    base_mana = models.IntegerField(default=100)
    base_max_mana = models.IntegerField(default=100)
    base_strength = models.IntegerField(default=10)
    base_intelligence = models.IntegerField(default=10)
    base_agility = models.IntegerField(default=10)

    sustained_damage = models.IntegerField(default=0)
    depleted_mana = models.IntegerField(default=0)

    def get_item_bonus(self, stat):
        stat_bonus = 0
        effective_items = self.character.items.filter(boosted_stat=stat)

        for item in effective_items:
            stat_bonus += item.value

        return stat_bonus

    @property
    def health(self):
        hp = self.base_health + self.get_item_bonus("health") - self.sustained_damage
        return hp if hp > 0 else 0

    @property
    def max_health(self):
        return self.base_max_health + self.get_item_bonus("health")

    @property
    def mana(self):
        mn = self.base_mana + self.get_item_bonus("mana") - self.depleted_mana
        return mn if mn > 0 else 0

    @property
    def max_mana(self):
        return self.base_max_mana + self.get_item_bonus("mana")

    @property
    def strength(self):
        return self.base_strength + self.get_item_bonus("strength")

    @property
    def intelligence(self):
        return self.base_intelligence + self.get_item_bonus("intelligence")

    @property
    def agility(self):
        return self.base_agility + self.get_item_bonus("agility")

    @property
    def is_dead(self):
        return self.health <= 0


class Quest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Character(models.Model):
    name = models.CharField(max_length=100)
    character_class = models.ForeignKey(
        CharacterClass, on_delete=models.PROTECT, related_name="characters"
    )
    statistics = models.OneToOneField(
        Statistics, on_delete=models.PROTECT, related_name="character"
    )
    guild = models.ForeignKey(Guild, on_delete=models.PROTECT, related_name="characters")
    gold = models.PositiveIntegerField(default=0)
    quests = models.ManyToManyField(Quest, related_name="characters")
    level = models.PositiveSmallIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    max_experience = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.character_class} {self.name} [Lv. {self.level}]"

    def check_level_up(self):
        if self.experience < self.max_experience:
            return False

        self.level += 1
        self.experience = 0
        self.max_experience *= 2

        return True


class Rarity(models.Model):
    COLOR_PALETTE = [
        (
            "#287d38",
            "green",
        ),
        (
            "#305bd1",
            "blue",
        ),
        (
            "#631e9c",
            "purple",
        ),
        (
            "#ed9f32",
            "orange",
        ),
    ]

    name = models.CharField(max_length=100)
    grade = models.PositiveSmallIntegerField()
    color = ColorField(samples=COLOR_PALETTE)

    def __str__(self):
        return self.name


class StatisticsChoices(models.TextChoices):
    health = ("health", "Health")
    mana = ("mana", "Mana")
    strength = ("strength", "Strength")
    intelligence = ("intelligence", "Intelligence")
    agility = ("agility", "Agility")


class Item(models.Model):
    name = models.CharField(max_length=100)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT, related_name="items")
    boosted_stat = models.CharField(max_length=20, choices=StatisticsChoices.choices)
    value = models.IntegerField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="items")
    icon = models.ImageField(upload_to="items/", null=True, blank=True)

    def __str__(self):
        return self.name
