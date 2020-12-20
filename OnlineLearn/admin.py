from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (_('Privacy info'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'header','biography', 'birthday', 'gender','profile_pic')}),
        (_('Social Media'), {'fields': ('linkedn', 'facebook')}),
        (_('Permissions'), {'fields': ('is_instructor', 'is_active', 'is_staff', 'is_superuser',)}),
        (_('Courses'), {'fields': ('taken_courses',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_instructor'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'gender','is_staff', 'is_instructor')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class LectureAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General Information'), {"fields":('text', 'type')}),
        (_('Resources (Please specify the field that you choose in the type)'), {'fields':('video_link', 'quiz','information')}),
        )

    list_display = ('text', 'type')


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Course)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Section)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Exam)
admin.site.register(Form_Answer)
admin.site.register(Form_Question)
admin.site.register(QA)
