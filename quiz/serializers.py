from rest_framework import serializers
from .models import *
from deep_translator import GoogleTranslator  # for automatic translation
from rest_framework.exceptions import ValidationError
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'page', 'title_en', 'content']


class QuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.CharField(required=False, allow_blank=True)
    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(), required=False
    )  # optional for direct POST
    options = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    options_output = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "quiz",
            "question",
            "qus_time",
            "options",
            "options_output",
            "correct_answer",
            "explain"
        ]

    def validate(self, data):
        quiz = data.get("quiz") or getattr(self.instance, "quiz", None)
        question_text = data.get("question", "").strip()

        if quiz:
            qs = Question.objects.filter(quiz=quiz, question__iexact=question_text)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise ValidationError(f"Question '{question_text}' already exists in this quiz.")
        return data

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        question = Question.objects.create(**validated_data)
        for opt_text in options_data:
            Option.objects.create(question=question, option_text=opt_text)
        return question

    def update(self, instance, validated_data):
        # Update basic fields
        for attr, value in validated_data.items():
            if attr != "options":
                setattr(instance, attr, value)
        instance.save()

        # Update options if provided
        options_data = validated_data.get("options")
        if options_data is not None:
            # Delete old options
            instance.options.all().delete()
            # Create new options
            for opt_text in options_data:
                Option.objects.create(question=instance, option_text=opt_text)

        return instance

    def get_options_output(self, instance):
        return [opt.option_text for opt in instance.options.all()]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        options_list = rep.pop("options_output", [])
        return {
            "id": rep["id"],
            "quiz": rep.get("quiz"),
            "question": rep["question"],
            "qus_time": rep.get("qus_time"),
            "options": options_list,
            "correct_answer": rep.get("correct_answer"),
            "explain": rep.get("explain")
        }


# class QuizSerializer(serializers.ModelSerializer):
#     all_questions = QuestionSerializer(many=True)
#     instruction = InstructionSerializer(many=True)

#     class Meta:
#         model = Quiz
#         fields = ['id', 'title', 'description', 'timer_duration', 'total_questions', 'instruction', 'all_questions']

#     def create(self, validated_data):
#         instructions_data = validated_data.pop('instruction', [])
#         questions_data = validated_data.pop('all_questions', [])
#         quiz = Quiz.objects.create(**validated_data)

#         # Add instructions
#         for instr_data in instructions_data:
#             instr, created = Instruction.objects.get_or_create(**instr_data)
#             quiz.instruction.add(instr)

#         # Add questions
#         for ques_data in questions_data:
#             options_data = ques_data.pop('options', [])  # safely pop options
#             ques_data.pop('quiz', None)  # remove quiz key if exists
#             question = Question.objects.create(quiz=quiz, **ques_data)

#             # Create options
#             for opt_text in options_data:
#                 Option.objects.create(question=question, option_text=opt_text)

#         return quiz

class QuizSerializer(serializers.ModelSerializer):
    all_questions = QuestionSerializer(many=True)
    instruction = InstructionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'timer_duration', 'total_questions',"can_see_explanation",
            "instant_feedback", 'instruction', 'all_questions']

    def create(self, validated_data):
        instructions_data = validated_data.pop('instruction', [])
        questions_data = validated_data.pop('all_questions', [])
        quiz = Quiz.objects.create(**validated_data)

        # Add instructions
        for instr_data in instructions_data:
            instr, created = Instruction.objects.get_or_create(**instr_data)
            quiz.instruction.add(instr)

        # Calculate time per question
        total_questions = len(questions_data)
        total_time = quiz.timer_duration or 0
        per_question_time = total_time // total_questions if total_questions > 0 else 0

        # Add questions
        for ques_data in questions_data:
            options_data = ques_data.pop('options', [])  # safely pop options
            ques_data.pop('quiz', None)  # remove quiz key if exists

            # Set qus_time if not provided
            if not ques_data.get('qus_time'):
                ques_data['qus_time'] = per_question_time

            question = Question.objects.create(quiz=quiz, **ques_data)

            # Create options
            for opt_text in options_data:
                Option.objects.create(question=question, option_text=opt_text)

        return quiz



class QuizListSerializer(serializers.ModelSerializer):
    instruction = serializers.SerializerMethodField()
    total_instruction_pages = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "timer_duration", "total_questions","total_instruction_pages","can_see_explanation",
            "instant_feedback", "instruction"]

    def get_instruction(self, obj):
        # Include the ID so you can update the instruction later
        return [
            {
                "id": ins.id,  # <--- instruction PK
                "page": ins.page,
                "title_en": ins.title_en,
                "content": ins.content
            }
            for ins in obj.instruction.all()
        ]
    
    def get_total_instruction_pages(self, obj):
        # Return the highest page number among instructions
        pages = obj.instruction.values_list('page', flat=True)
        return max(pages) if pages else 0


class BannerSerializer(serializers.ModelSerializer):
    quiz_title = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()  # for nested quiz info
    quiz_id = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(), source='quiz', write_only=True, required=False
    )

    # Make Bangla fields read-only; they will be auto-translated
    title_bangla = serializers.CharField(read_only=True)
    subtitle_bangla = serializers.CharField(read_only=True)
    button_bangla = serializers.CharField(read_only=True)

    class Meta:
        model = Banner
        # Exclude 'page' if you don't need it
        exclude = ('page', )

    def get_quiz_title(self, obj):
        return obj.quiz.title if obj.quiz else ""

    def get_quiz(self, obj):
        if obj.quiz:
            return {"id": obj.quiz.id, "title": obj.quiz.title}
        return {"id": None, "title": None}

    def create(self, validated_data):
        # Auto-translate English fields to Bangla
        if 'title_english' in validated_data:
            validated_data['title_bangla'] = GoogleTranslator(source='en', target='bn').translate(validated_data['title_english'])
        if 'subtitle_english' in validated_data:
            validated_data['subtitle_bangla'] = GoogleTranslator(source='en', target='bn').translate(validated_data['subtitle_english'])
        if 'button_english' in validated_data:
            validated_data['button_bangla'] = GoogleTranslator(source='en', target='bn').translate(validated_data['button_english'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Auto-translate on update
        if 'title_english' in validated_data:
            instance.title_bangla = GoogleTranslator(source='en', target='bn').translate(validated_data['title_english'])
        if 'subtitle_english' in validated_data:
            instance.subtitle_bangla = GoogleTranslator(source='en', target='bn').translate(validated_data['subtitle_english'])
        if 'button_english' in validated_data:
            instance.button_bangla = GoogleTranslator(source='en', target='bn').translate(validated_data['button_english'])
        return super().update(instance, validated_data)


class InstructionNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Instruction
        fields = ['id', 'page', 'title_en', 'content']
        # extra_kwargs = {'id': {'read_only': False}}  # allow using id for updates

# class QuizDetailSerializer(serializers.ModelSerializer):
#     instructions = InstructionNestedSerializer(many=True, source='instruction')
#     total_instruction_pages = serializers.SerializerMethodField()

#     class Meta:
#         model = Quiz
#         fields = ["id", "title", "description", "timer_duration", "total_questions","total_instruction_pages", "instructions"]
        

#     def update(self, instance, validated_data):
#         # Get instructions from validated_data if provided
#         instructions_data = validated_data.pop('instruction', None)

#         with transaction.atomic():
#             if instructions_data is not None:
#                 # Option 1: Replace all instructions
#                 instance.instruction.clear()

#             # Add new instructions
#             for instr_data in instructions_data:
#                 # Remove 'id' if present to avoid UNIQUE errors
#                 instr_data.pop('id', None)
#                 instr = Instruction.objects.create(**instr_data)
#                 instance.instruction.add(instr)

#         # Update other quiz fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         return instance
    

#     def get_total_instruction_pages(self, obj):
#         # Return the highest page number among instructions
#         pages = obj.instruction.values_list('page', flat=True)
#         return max(pages) if pages else 0


class QuizDetailSerializer(serializers.ModelSerializer):
    instructions = InstructionNestedSerializer(many=True, source='instruction')
    total_instruction_pages = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "timer_duration",
            "total_questions",
            "total_instruction_pages",
            "can_see_explanation",
            "instant_feedback",
            "instructions"
        ]

    def create(self, validated_data):
        instructions_data = validated_data.pop('instruction', [])

        with transaction.atomic():
            # Create the quiz
            quiz = Quiz.objects.create(**validated_data)

            # Create instructions
            for instr_data in instructions_data:
                instr_data.pop('id', None)  # remove id if present
                instr = Instruction.objects.create(**instr_data)
                quiz.instruction.add(instr)

        return quiz

    def update(self, instance, validated_data):
        instructions_data = validated_data.pop('instructions', None)

        with transaction.atomic():
            # Update other quiz fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if instructions_data is not None:
                # Clear existing instructions
                instance.instruction.clear()
                # Add new instructions
                for instr_data in instructions_data:
                    instr_data.pop('id', None)
                    instr = Instruction.objects.create(**instr_data)
                    instance.instruction.add(instr)

        return instance

    def get_total_instruction_pages(self, obj):
        pages = obj.instruction.values_list('page', flat=True)
        return max(pages) if pages else 0



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
        new_rep = {}
        for key in [
            "id", "quizzes", "name", "description", "monthly_price", "yearly_price",
            "popular", "features", "button_text", "button_variant", "color", "icon"
        ]:
            if key == "features":
                new_rep[key] = features_list
            else:
                new_rep[key] = rep.get(key)
        return new_rep