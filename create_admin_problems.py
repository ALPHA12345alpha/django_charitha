#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

from django.contrib.auth.models import User
from problems.models import Problem, TestCase

admin_user = User.objects.get(username='admin')

# Add more sample problems
problems = [
    {
        'title': 'Add Two Numbers',
        'description': 'Given two integers a and b, return their sum.',
        'input_format': 'Two integers a and b on separate lines.',
        'output_format': 'The sum of a and b.',
        'constraints': '-1000 <= a, b <= 1000',
        'sample_input': '5\n3',
        'sample_output': '8',
        'difficulty': 'easy',
        'test_cases': [
            ('5\n3', '8'),
            ('10\n-5', '5'),
            ('0\n0', '0')
        ]
    },
    {
        'title': 'Maximum of Three',
        'description': 'Find the maximum of three given numbers.',
        'input_format': 'Three integers on separate lines.',
        'output_format': 'The maximum number.',
        'constraints': '-100 <= numbers <= 100',
        'sample_input': '10\n5\n8',
        'sample_output': '10',
        'difficulty': 'easy',
        'test_cases': [
            ('10\n5\n8', '10'),
            ('1\n2\n3', '3'),
            ('-1\n-2\n-3', '-1')
        ]
    }
]

for prob_data in problems:
    test_cases = prob_data.pop('test_cases')
    problem, created = Problem.objects.get_or_create(
        title=prob_data['title'],
        defaults={**prob_data, 'created_by': admin_user}
    )
    
    if created:
        for i, (input_data, expected_output) in enumerate(test_cases):
            TestCase.objects.create(
                problem=problem,
                input_data=input_data,
                expected_output=expected_output,
                is_sample=(i == 0)
            )

print("Additional problems created!")