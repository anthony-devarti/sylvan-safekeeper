from rest_framework import serializers
from library.models import ReservationStatus


class ReservationStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    desc = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `ReservationStatus` instance, given the validated data.
        """
        return ReservationStatus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `ReservationStatus` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance