from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Submission, Contest
from .forms import SubmissionForm, ContestForm
from problems.models import Problem
from .judge import judge_submission
import threading

class SubmissionCreateView(LoginRequiredMixin, View):
    def post(self, request, problem_id):
        problem = get_object_or_404(Problem, pk=problem_id)
        form = SubmissionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.problem = problem
            sub.status = "PENDING"
            sub.save()
            
            # Judge submission in background
            thread = threading.Thread(target=judge_submission, args=(sub.id,))
            thread.start()
            
            messages.success(request, 'Code submitted successfully!')
            return redirect("submission_detail", pk=sub.pk)
        else:
            messages.error(request, 'Please fix the errors in your submission.')
            return redirect('problem_detail', pk=problem_id)

class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "submissions/submission_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only show submission details to the owner or staff
        if self.object.user != self.request.user and not self.request.user.is_staff:
            context['hide_code'] = True
        return context

class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "submissions/submission_list.html"
    context_object_name = 'submissions'
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_staff:
            return Submission.objects.all().order_by("-created_at")
        return Submission.objects.filter(user=self.request.user).order_by("-created_at")

class ContestListView(LoginRequiredMixin, ListView):
    model = Contest
    template_name = 'contests/contest_list.html'
    context_object_name = 'contests'
    paginate_by = 10
    
    def get_queryset(self):
        return Contest.objects.filter(is_public=True)

class ContestDetailView(LoginRequiredMixin, DetailView):
    model = Contest
    template_name = 'contests/contest_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = self.object.problems.all()
        return context

class ContestCreateView(LoginRequiredMixin, CreateView):
    model = Contest
    form_class = ContestForm
    template_name = 'contests/contest_create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Contest created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'/contests/{self.object.pk}/'

def submission_status(request, submission_id):
    """AJAX endpoint to check submission status"""
    try:
        submission = get_object_or_404(Submission, id=submission_id, user=request.user)
        return JsonResponse({
            'status': submission.status,
            'output': submission.output,
            'execution_time': submission.execution_time,
            'judged_at': submission.judged_at.isoformat() if submission.judged_at else None
        })
    except:
        return JsonResponse({'error': 'Submission not found'}, status=404)
