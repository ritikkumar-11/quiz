from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def role_required(role_check, login_url='login', redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Generic decorator for views that checks whether the logged-in user meets
    the role condition provided by `role_check` function. Redirects to the
    login page if necessary.
    
    Args:
        role_check (function): A function that takes a user object and returns True if the user has the required role.
        login_url (str): The URL to redirect to if the user does not meet the condition.
        redirect_field_name (str): The name of a GET field containing the URL to redirect to after login.
    
    Returns:
        function: The actual decorator.
    """
    return user_passes_test(
        lambda u: u.is_active and role_check(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged-in user is a student,
    and redirects to the login page if necessary.
    
    Args:
        function (function): The view function to be decorated.
        redirect_field_name (str): The name of a GET field containing the URL to redirect to after login.
        login_url (str): The URL to redirect to if the user does not meet the condition.
    
    Returns:
        function: The decorated view function.
    """
    actual_decorator = role_required(lambda u: u.is_student, login_url, redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator

def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged-in user is a teacher,
    and redirects to the login page if necessary.
    
    Args:
        function (function): The view function to be decorated.
        redirect_field_name (str): The name of a GET field containing the URL to redirect to after login.
        login_url (str): The URL to redirect to if the user does not meet the condition.
    
    Returns:
        function: The decorated view function.
    """
    actual_decorator = role_required(lambda u: u.is_teacher, login_url, redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator
