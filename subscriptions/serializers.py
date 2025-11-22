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
    # features = FeatureSerializer(many=True, write_only=True)  # for input
    # features_read = FeatureSerializer(many=True, read_only=True, source='features')  # for output
    
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    # features_list = serializers.SerializerMethodField(read_only=True)

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
            "title",
            "description",
            "monthly_price",
            "yearly_price",
            "month",
            "year",
            "popular",
            "discount",
            "choice",
            # "discount_type",
            "monthly_discount",
            "yearly_discount",
            # "features_read",
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
        
        quizzes_list = [{"id": q.id, "title": q.title, "description": q.description} for q in instance.quizzes.all()]

        new_rep = {}
        for key in [
            "id",  "title", "description", "monthly_price", "yearly_price","month", "year", 'discount',"choice","monthly_discount",
            "yearly_discount",
            "popular", "features", "quizzes"
        ]:
            if key == "features":
                new_rep[key] = features_list

            elif key == "quizzes":
                new_rep[key] = quizzes_list
            else:
                new_rep[key] = rep.get(key)
        return new_rep
    

# User = get_user_model()

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    # mobile = serializers.CharField(source="user.mobile", read_only=True)
    mobile = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), write_only=True, source='plan'
    )
    
    

    class Meta:
        model = UserSubscription
        fields = ['id', 'user',"mobile", 'plan', 'plan_id','start_date', 'end_date', 'active']
    
    # for creating subscription
    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data.pop('plan')
        

        subscription = UserSubscription.objects.create(user=user, plan=plan, **validated_data)
        return subscription
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        
        rep["plan_title"] = instance.plan.title if instance.plan else None
        
        # rep["discounted_monthly_price"] = instance.discounted_price('month')
        # rep["discounted_yearly_price"] = instance.discounted_price('year')

        return rep