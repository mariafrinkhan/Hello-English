from django.db import models
from django.contrib.auth.models import User
from deep_translator import GoogleTranslator
from django_ckeditor_5.fields import CKEditor5Field


class Banner(models.Model):
    quiz = models.ForeignKey('Quiz', related_name='banners', null=True, blank=True, on_delete=models.SET_NULL)

    # english inputs (what user will provide)
    title_english = models.CharField(max_length=255)
    subtitle_english = models.TextField(blank=True, null=True)
    button_english = models.CharField(max_length=100, blank=True, null=True)

    # bangla fields (auto-filled when blank)
    title_bangla = models.CharField(max_length=255, blank=True, null=True)
    subtitle_bangla = models.TextField(blank=True, null=True)
    button_bangla = models.CharField(max_length=100, blank=True, null=True)

    page = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='assets/uploads/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def save(self, *args, **kwargs):
        translator = GoogleTranslator(source='en', target='bn')

        if not self.title_bangla and self.title_english:
            self.title_bangla = translator.translate(self.title_english)

        if not self.subtitle_bangla and self.subtitle_english:
            self.subtitle_bangla = translator.translate(self.subtitle_english)

        if not self.button_bangla and self.button_english:
            self.button_bangla = translator.translate(self.button_english)


        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_english


class Instruction(models.Model):
    # quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='instructions', null=True, blank=True)
    page = models.PositiveIntegerField(null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    # contents = JSONField(default=list, blank=True)  # stores list of strings
    content = CKEditor5Field(config_name='extends', blank=True, null=True)

    def __str__(self):
        return f"Instruction Title: {self.title_en or 'Untitled'}"
    
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timer_duration = models.PositiveIntegerField(default=0)  # in minutes
    total_questions = models.PositiveIntegerField(default=0, null=True, blank=True)
    instruction = models.ManyToManyField(Instruction, blank=True)
    can_see_explanation = models.BooleanField(null=True, blank=True)
    instant_feedback= models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="all_questions", on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    qus_time = models.PositiveIntegerField(null=True, blank=True)
    explain = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question


class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2)
    popular = models.BooleanField(default=False)
    button_text = models.CharField(max_length=100, blank=True)
    button_variant = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, blank=True)
    icon = models.CharField(max_length=100, blank=True)

    quizzes = models.ManyToManyField('quiz.Quiz', related_name='plans', blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    plan = models.ForeignKey(Plan, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text