from rest_framework import serializers
from .models import *
from deep_translator import GoogleTranslator  # for automatic translation
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth import get_user_model

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['text']

class PlanSerializer(serializers.ModelSerializer):
    # Input field for features (write-only)
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    quizzes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Quiz.objects.all(),
        required=False
    )

    class Meta:
        model = Plan
        fields = [
            "id",
            "quizzes",
            "name",
            "description",
            "monthly_price",
            "yearly_price",
            "month",
            "year",
            "popular",
            "button_text",
            "button_variant",
            "color",
            "icon",
            "features"
        ]

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        quizzes_data = validated_data.pop('quizzes', [])
        plan = Plan.objects.create(**validated_data)
        for feature_text in features_data:
            Feature.objects.create(plan=plan, text=feature_text)

        # Assign quizzes using .set()
        if quizzes_data:
            plan.quizzes.set(quizzes_data)

        

        return plan
    


    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', None)
        quizzes_data = validated_data.pop('quizzes', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if features_data is not None:
            instance.features.all().delete()
            for feature_text in features_data:
                Feature.objects.create(plan=instance, text=feature_text)

        if quizzes_data is not None:
            instance.quizzes.set(quizzes_data)

        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Insert features after 'popular'
        features_list = [f.text for f in instance.features.all()]
        
        quizzes_list = [{"id": q.id, "title": q.title} for q in instance.quizzes.all()]

        new_rep = {}
        for key in [
            "id", "quizzes", "name", "description", "monthly_price", "yearly_price","month", "year",
            "popular", "features", "button_text", "button_variant", "color", "icon"
        ]:
            if key == "features":
                new_rep[key] = features_list

            elif key == "quizzes":
                new_rep[key] = quizzes_list
            else:
                new_rep[key] = rep.get(key)
        return new_rep
    

User = get_user_model()

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    mobile = serializers.CharField(source="user.mobile", read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), write_only=True, source='plan'
    )

    class Meta:
        model = UserSubscription
        fields = ['id', 'user',"mobile", 'plan', 'plan_id', 'start_date', 'end_date', 'active']
# for creating subscription
    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data.pop('plan')
        subscription = UserSubscription.objects.create(user=user, plan=plan)
        return subscription
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        
        rep["plan_title"] = instance.plan.name if instance.plan else None

        return rep