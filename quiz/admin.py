from django.contrib import admin
from .models import *


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title_english', 'subtitle_english', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title_english']
    ordering = ['-created_at']

# class ContentInline(admin.TabularInline):  # or use admin.StackedInline for vertical layout
#     model = Content
#     extra = 1

@admin.register(Instruction)
class InstructionTitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_en', 'page']  
    search_fields = ['title_en']


# @admin.register(Content)
# class ContentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'ins_title_en', 'content_en']
#     search_fields = ['content_en']
#     list_filter = ['ins_title_en']



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'timer_duration', 'total_questions')
    search_fields = ('title',)
    list_filter = ('timer_duration',)
    filter_horizontal = ('instruction',)