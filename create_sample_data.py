#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

from django.contrib.auth.models import User
from problems.models import Problem, TestCase
from submissions.models import Contest

# Create sample problems
problems_data = [
    {
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
        'input_format': 'First line contains n (number of elements). Second line contains n integers. Third line contains target.',
        'output_format': 'Two space-separated integers representing the indices.',
        'constraints': '2 <= n <= 10^4, -10^9 <= nums[i] <= 10^9',
        'sample_input': '4\n2 7 11 15\n9',
        'sample_output': '0 1',
        'difficulty': 'easy',
        'time_limit': 1.0,
        'memory_limit': 128
    },
    {
        'title': 'Fibonacci Number',
        'description': 'Calculate the nth Fibonacci number.',
        'input_format': 'A single integer n.',
        'output_format': 'The nth Fibonacci number.',
        'constraints': '0 <= n <= 30',
        'sample_input': '10',
        'sample_output': '55',
        'difficulty': 'easy',
        'time_limit': 1.0,
        'memory_limit': 128
    },
    {
        'title': 'Binary Search',
        'description': 'Find the position of target in a sorted array using binary search.',
        'input_format': 'First line contains n. Second line contains n sorted integers. Third line contains target.',
        'output_format': 'Index of target (0-based) or -1 if not found.',
        'constraints': '1 <= n <= 10^5, -10^9 <= arr[i] <= 10^9',
        'sample_input': '5\n1 3 5 7 9\n5',
        'sample_output': '2',
        'difficulty': 'medium',
        'time_limit': 2.0,
        'memory_limit': 256
    }
]

admin_user = User.objects.get(username='admin')

for prob_data in problems_data:
    problem, created = Problem.objects.get_or_create(
        title=prob_data['title'],
        defaults={**prob_data, 'created_by': admin_user}
    )
    
    if created:
        # Create test cases
        if prob_data['title'] == 'Two Sum':
            TestCase.objects.create(
                problem=problem,
                input_data='4\n2 7 11 15\n9',
                expected_output='0 1',
                is_sample=True
            )
        elif prob_data['title'] == 'Fibonacci Number':
            TestCase.objects.create(
                problem=problem,
                input_data='10',
                expected_output='55',
                is_sample=True
            )
        elif prob_data['title'] == 'Binary Search':
            TestCase.objects.create(
                problem=problem,
                input_data='5\n1 3 5 7 9\n5',
                expected_output='2',
                is_sample=True
            )

print("Sample data created successfully!")