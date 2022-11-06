from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'
    # list_students = Student.objects.all().order_by(ordering)
    list_students = Student.objects.all().prefetch_related('teachers').order_by(ordering)

    context = {'object_list': list_students}

    return render(request, template, context)
