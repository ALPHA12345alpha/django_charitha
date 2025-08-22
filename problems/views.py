from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Problem
from submissions.forms import ProblemForm, SubmissionForm
from submissions.models import Submission

class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    template_name = "problems/problem_list.html"
    context_object_name = 'problems'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Problem.objects.filter(is_active=True)
        search = self.request.GET.get('search')
        difficulty = self.request.GET.get('difficulty')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['difficulties'] = Problem.DIFFICULTY_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        return context

class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = "problems/problem_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission_form'] = SubmissionForm()
        context['user_submissions'] = Submission.objects.filter(
            user=self.request.user, 
            problem=self.object
        ).order_by('-created_at')[:5]
        return context

class ProblemCreateView(LoginRequiredMixin, CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'problems/problem_create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Problem created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'/problems/{self.object.pk}/'

def leaderboard(request):
    # Get top users by problems solved
    from django.contrib.auth.models import User
    from django.db.models import Count
    
    users = User.objects.annotate(
        solved_count=Count('submission', filter=Q(submission__status='AC'))
    ).order_by('-solved_count')[:20]
    
    return render(request, 'problems/leaderboard.html', {'users': users})
