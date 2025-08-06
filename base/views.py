from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Course, Review, Standard, Registration

# Create your views here.
def redirectCurrent(request):
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def home(request):
    courses = Course.objects.prefetch_related('standards').all()
    classes = Standard.objects.all()
    reviews = Review.objects.order_by('-rating')[:5]

    course_data = []
    for course in courses:
        course_data.append({
            'id': course.id,
            'name': course.name,
            'description': course.desc,
            'rating': course.rating,
            'range': course.class_range(),  # e.g., "6-12"
        })
    
    return render(request, 'base/home.html', {'courses': course_data, 'classes':classes, 'reviews':reviews})

def aboutUs(request):
    courses = Course.objects.all()
    classes = Standard.objects.all()

    return render(request, 'base/about-us.html', {'courses': courses, 'classes':classes})

def courses(request):
    courses = Course.objects.prefetch_related('standards').all()
    classes = Standard.objects.all()

    return render(request, 'base/courses.html', {'courses': courses, 'classes':classes})

@require_POST
def registeration(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    contact = request.POST.get('contact')
    course_id = request.POST.get('course')
    class_id = request.POST.get('class')
    query = request.POST.get('text', '')


    if not all([name, email, contact, course_id, class_id]):
        messages.error(request, 'All fields required')
        return redirectCurrent(request)
    
    try:
        course_name = Course.objects.get(id=course_id).name
        class_name = Standard.objects.get(id=class_id).name
    except Exception as e:
        messages.error(request, 'Course or class not found!')

    Registration.objects.create(
        name=name,
        email=email,
        contact=contact,
        course=course_name,
        class_name=class_name,
        query=query
    )

    messages.success(request, 'Successfully registered! We will get back to you soon!')

    return redirectCurrent(request)