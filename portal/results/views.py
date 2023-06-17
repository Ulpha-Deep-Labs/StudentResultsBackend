from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import StudentLoginForm, AddResultForm, SelectCourseForm, ScoreForm
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    # Retrieve the user profile information
    user_profile = models.Student.objects.get(user=request.user)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'results/dashboard.html', context)

@login_required
def score_form_view(request, course_id):
    ScoreFormSet = formset_factory(ScoreForm, extra=0)
    course = models.Course.objects.get(id=course_id)
    students = models.Student.objects.filter(courseitem__course=course).order_by('department')

    if request.method == "POST":
        formset = ScoreFormSet(request.POST)

        if formset.is_valid():
            formset.save()
            return redirect("sucess.html")
        
    else:
        initial_data = [{'student': student, 
                         'CA Score': student.courseitem__student_course_ca,
                         'Exam Score': student.courseitem__student_course_exam_score,
                         } for student in students]
        formset = ScoreFormSet(initial_data=initial_data)
        context = {
            "formset": formset,
            'course': course,
        }
    return render(request, 'score_form.html', context)



