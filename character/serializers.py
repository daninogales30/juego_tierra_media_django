from rest_framework import serializers
from .models import Relacion
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
        depth = 1

class RelacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relacion
        fields = ['id', 'character', 'related_to', 'tipo', 'confidence_level']

    def validate(self, data):
        if data.get('character') == data.get('related_to'):
            raise serializers.ValidationError("Un personaje no puede relacionarse consigo mismo.")
        return data
