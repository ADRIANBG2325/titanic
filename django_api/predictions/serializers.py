from rest_framework import serializers


class PredictionInputSerializer(serializers.Serializer):
    """Serializer for prediction input data"""
    pclass = serializers.IntegerField(min_value=1, max_value=3)
    sex = serializers.ChoiceField(choices=['male', 'female'])
    age = serializers.FloatField(min_value=0, max_value=100)
    sibsp = serializers.IntegerField(min_value=0)
    parch = serializers.IntegerField(min_value=0)
    fare = serializers.FloatField(min_value=0)
    embarked = serializers.ChoiceField(choices=['C', 'Q', 'S'])
    name = serializers.CharField(required=False, allow_blank=True)
    ticket = serializers.CharField(required=False, allow_blank=True)
    cabin = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        """Additional validation"""
        if data['age'] < 0 or data['age'] > 100:
            raise serializers.ValidationError("Age must be between 0 and 100")
        if data['fare'] < 0:
            raise serializers.ValidationError("Fare must be positive")
        return data


class PredictionOutputSerializer(serializers.Serializer):
    """Serializer for prediction output"""
    survived = serializers.BooleanField()
    probability = serializers.FloatField()
    survival_chance = serializers.CharField()
    model_type = serializers.CharField()
    model_accuracy = serializers.FloatField()
    features_used = serializers.ListField(child=serializers.CharField())
