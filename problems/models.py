from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField(default='Input description not provided')
    output_format = models.TextField(default='Output description not provided')
    constraints = models.TextField(default='No constraints specified')
    sample_input = models.TextField(default='No sample input')
    sample_output = models.TextField(default='No sample output')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    time_limit = models.FloatField(default=2.0)
    memory_limit = models.IntegerField(default=256)  # MB
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_acceptance_rate(self):
        total = self.submission_set.count()
        if total == 0:
            return 0
        accepted = self.submission_set.filter(status='AC').count()
        return round((accepted / total) * 100, 1)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="testcases")
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)
    points = models.IntegerField(default=10)

    def __str__(self):
        return f"TestCase for {self.problem.title}"
