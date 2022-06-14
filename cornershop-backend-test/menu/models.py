import uuid
from datetime import date

from django.db import models


class Menu(models.Model):
    """
    Menu model, uses UUID as primary key
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(default="Lunch")
    date = models.DateField(default=date.today)


class MenuOption(models.Model):
    """
    Meal option for a specific Menu instance
    """

    menu = models.ForeignKey("Menu", on_delete=models.CASCADE, related_name="options")
    text = models.TextField()


class MenuResponse(models.Model):
    """
    Employee menu selection, related to the Menu and MenuOption instances
    """

    menu = models.ForeignKey("Menu", on_delete=models.CASCADE, related_name="responses")
    option = models.ForeignKey(
        "MenuOption", on_delete=models.CASCADE, related_name="responses"
    )
    employee = models.TextField()
    customization = models.TextField(blank=True)
