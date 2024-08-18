from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.db.models import Avg


from .models import Quiz, Question, Answer, Student, TakenQuiz, StudentAnswer
from .forms import TeacherSignUpForm, StudentSignUpForm, QuestionForm, TakeQuizForm

# Auth Views
class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        auth_logout(request)
        return redirect('home')

# Student Views
class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'students/quiz_list.html'
    
    def get_queryset(self):
        student = self.request.user.student
        return Quiz.objects.filter(subject__in=student.interests)

class TakenQuizListView(LoginRequiredMixin, ListView):
    model = TakenQuiz
    template_name = 'students/taken_quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        return TakenQuiz.objects.filter(student=student)

def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student
    unanswered_questions = student.get_unanswered_questions(quiz)

    if request.method == 'POST':
        form = TakeQuizForm(request.POST, question=unanswered_questions[0])
        if form.is_valid():
            answer = form.cleaned_data['answer']
            StudentAnswer.objects.create(student=student, answer=answer)
            if not unanswered_questions.exists():
                return redirect('students:taken_quiz_list')
            return redirect('students:take_quiz', pk=quiz.pk)
    else:
        form = TakeQuizForm(question=unanswered_questions[0])

    return render(request, 'students/take_quiz.html', {
        'quiz': quiz,
        'form': form,
        'question': unanswered_questions[0]
    })

# Teacher Views
class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'teachers/quiz_change_list.html'

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['name', 'subject']
    template_name = 'teachers/quiz_form.html'
    success_url = '/teachers/quizzes/'

class QuizUpdateView(LoginRequiredMixin, UpdateView):
    model = Quiz
    fields = ['name', 'subject']
    template_name = 'teachers/quiz_form.html'

class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    template_name = 'teachers/quiz_confirm_delete.html'
    success_url = '/teachers/quizzes/'

class QuizResultsView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'teachers/quiz_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object
        context['taken_quizzes'] = TakenQuiz.objects.filter(quiz=quiz)
        context['total_taken_quizzes'] = context['taken_quizzes'].count()
        context['quiz_score'] = TakenQuiz.objects.filter(quiz=quiz).aggregate(
            average_score=Avg('score')
        )
        return context

def question_add(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('teachers:quiz_change', pk=quiz.pk)
    else:
        form = QuestionForm()
    return render(request, 'teachers/question_form.html', {
        'form': form,
        'quiz': quiz
    })

def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('teachers:quiz_change', pk=quiz.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'teachers/question_form.html', {
        'form': form,
        'quiz': quiz,
        'question': question
    })

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'teachers/question_confirm_delete.html'

    def get_success_url(self):
        return reverse('teachers:quiz_change', kwargs={'pk': self.object.quiz.pk})

# Sign Up Views
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'user_type': 'student'})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'user_type': 'teacher'})
