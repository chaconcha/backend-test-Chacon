from rest_framework import serializers

from .models import Menu, MenuOption, MenuResponse


class MenuResponseSerializer(serializers.ModelSerializer):
    """
    Serializer used for saving the menu responses.
    """

    class Meta:
        model = MenuResponse
        fields = "__all__"


class MenuOptionSerializer(serializers.ModelSerializer):
    """
    Serializer used for listing the menu options.
    """

    class Meta:
        model = MenuOption
        fields = ["id", "text"]
        read_only_fields = ["id"]


class MenuResponseListSerializer(serializers.ModelSerializer):
    """
    Serializer used for listing the menu responses.
    """

    option = MenuOptionSerializer(read_only=True, required=False)

    class Meta:
        model = MenuResponse
        fields = "__all__"


class MenuDetailSerializer(serializers.ModelSerializer):
    """
    Serializer used for reading, creating and updating each menu.
    """

    options = MenuOptionSerializer(many=True, required=False)
    responses = MenuResponseListSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        Creates and returns 'Menu' and 'Options' instances,
        given the validated data.
        """
        options = validated_data.pop("options")

        menu = Menu.objects.create(**validated_data)
        for option_data in options:
            MenuOption.objects.create(menu=menu, **option_data)
        return menu

    def update(self, instance, validated_data):
        """
        Updates and return an existing 'Menu' instance.
        Related Options (and by consequence Responses) are erased and
        new ones are created.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.date = validated_data.get("date", instance.date)

        MenuOption.objects.filter(menu=instance).delete()
        options = validated_data.get("options")
        for option_data in options:
            MenuOption.objects.create(menu=instance, **option_data)

        return instance


class MenuSerializer(serializers.ModelSerializer):
    """
    Menu serializer used for reading menu fields and options,
    doesn't include responses.
    """

    options = MenuOptionSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = ["id", "name", "date", "options"]
        read_only_fields = fields
