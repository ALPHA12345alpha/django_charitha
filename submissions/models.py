from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem

class Submission(models.Model):
    LANGUAGES = [
        ("python", "Python"),
        ("cpp", "C++"),
        ("java", "Java"),
        ("javascript", "JavaScript"),
    ]
    STATUS = [
        ("PENDING", "Pending"),
        ("JUDGING", "Judging"),
        ("AC", "Accepted"),
        ("WA", "Wrong Answer"),
        ("CE", "Compilation Error"),
        ("RE", "Runtime Error"),
        ("TLE", "Time Limit Exceeded"),
        ("MLE", "Memory Limit Exceeded"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGES)
    status = models.CharField(max_length=10, choices=STATUS, default="PENDING")
    output = models.TextField(blank=True, null=True)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    judged_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.problem} ({self.status})"
    
    def get_status_color(self):
        colors = {
            'AC': 'success',
            'WA': 'danger', 
            'CE': 'warning',
            'RE': 'danger',
            'TLE': 'info',
            'MLE': 'info',
            'PENDING': 'secondary',
            'JUDGING': 'primary'
        }
        return colors.get(self.status, 'secondary')

class Contest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    problems = models.ManyToManyField(Problem)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_time <= now <= self.end_time
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return timezone.now() < self.start_time
