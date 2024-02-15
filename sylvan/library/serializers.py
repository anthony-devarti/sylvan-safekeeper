from rest_framework import serializers
from library.models import ReservationStatus, LineItem, Reservation, Delinquency, DecisionPoint, Case, ProblemLineItem
from django.contrib.auth.models import Group, User


class ReservationStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    desc = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `ReservationStatus` instance, given the validated data.
        """
        return ReservationStatus.objects.create(**validated_data)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields =  '__all__' 

class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=ReservationStatus.objects.all())
    action_required = serializers.PrimaryKeyRelatedField(queryset=DecisionPoint.objects.all())
    id = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Reservation
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id
        return data
    
# Have a separate serializer for cases so I don't have to deal with the representation differences 
class CaseReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class DelinquencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delinquency
        fields = '__all__'

class DecisionPointSerializer(serializers.HyperlinkedModelSerializer):
    destination_on_decline = serializers.StringRelatedField(source='destination_on_decline.name', read_only=True)
    destination_on_success = serializers.StringRelatedField(source='destination_on_success.name', read_only=True)
    
    class Meta:
        model = DecisionPoint
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id
        return data
    
class CaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class ProblemLineItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProblemLineItem
        fields = '__all__'