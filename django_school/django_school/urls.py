from django.urls import include, path
from classroom.views import classroom, students, teachers

urlpatterns = [
    path('', include('classroom.urls')),  # Includes URLs from the classroom app
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),  # Sign up route
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),  # Student sign-up route
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),  # Teacher sign-up route
    # path('account/logout/', )
]

