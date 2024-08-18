from django.urls import include, path
from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),  # Home page route

    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),  # List of quizzes for students
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),  # Student interests view
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),  # List of quizzes taken by the student
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),  # Route to take a quiz
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),  # List of quizzes for teachers
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),  # Route to add a quiz
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),  # Route to update a quiz
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),  # Route to delete a quiz
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),  # Route to view quiz results
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),  # Route to add a question to a quiz
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),  # Route to change a question
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),  # Route to delete a question
    ], 'classroom'), namespace='teachers')),
]
