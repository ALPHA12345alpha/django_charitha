#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

from problems.models import Problem, TestCase

# Fix Two Sum problem
two_sum = Problem.objects.filter(title='Two Sum').first()
if two_sum:
    TestCase.objects.filter(problem=two_sum).delete()
    TestCase.objects.create(
        problem=two_sum,
        input_data='4\n2 7 11 15\n9',
        expected_output='0 1',
        is_sample=True
    )
    TestCase.objects.create(
        problem=two_sum,
        input_data='3\n3 2 4\n6',
        expected_output='1 2',
        is_sample=False
    )

# Fix Fibonacci problem  
fib = Problem.objects.filter(title='Fibonacci Number').first()
if fib:
    TestCase.objects.filter(problem=fib).delete()
    TestCase.objects.create(
        problem=fib,
        input_data='0',
        expected_output='0',
        is_sample=True
    )
    TestCase.objects.create(
        problem=fib,
        input_data='1',
        expected_output='1',
        is_sample=False
    )
    TestCase.objects.create(
        problem=fib,
        input_data='10',
        expected_output='55',
        is_sample=False
    )

# Add a simple Hello World problem
hello_world, created = Problem.objects.get_or_create(
    title='Hello World',
    defaults={
        'description': 'Print "Hello World" to the console.',
        'input_format': 'No input required.',
        'output_format': 'Print "Hello World" (without quotes).',
        'constraints': 'None',
        'sample_input': '',
        'sample_output': 'Hello World',
        'difficulty': 'easy',
        'time_limit': 1.0,
        'memory_limit': 128
    }
)

if created:
    TestCase.objects.create(
        problem=hello_world,
        input_data='',
        expected_output='Hello World',
        is_sample=True
    )

print("Sample problems fixed!")