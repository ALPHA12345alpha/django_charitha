from django.contrib import admin
from .models import Problem, TestCase

# Register your models here.

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "time_limit")
    inlines = [TestCaseInline]

admin.site.register(TestCase)
