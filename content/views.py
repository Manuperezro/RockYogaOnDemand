from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Course

# Create your views here.

def course_list(request):
    """ A view to show all courses, including sorting and searching queries """

    courses = Course.objects.all()
    print('courses', courses)
    context = {
        'courses': courses,
    }
    return render(request, 'content/course_list.html', context)
