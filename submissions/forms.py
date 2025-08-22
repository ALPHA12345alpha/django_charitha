from django import forms
from .models import Submission, Contest
from problems.models import Problem

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["code", "language"]
        widgets = {
            "code": forms.Textarea(attrs={
                "rows": 15, 
                "class": "form-control",
                "placeholder": "Write your code here..."
            }),
            "language": forms.Select(attrs={"class": "form-select"}),
        }

class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'description', 'start_time', 'end_time', 'problems', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'problems': forms.CheckboxSelectMultiple(),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'input_format', 'output_format', 
                 'constraints', 'sample_input', 'sample_output', 'difficulty', 
                 'time_limit', 'memory_limit']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'input_format': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'output_format': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'constraints': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sample_input': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sample_output': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'memory_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }
