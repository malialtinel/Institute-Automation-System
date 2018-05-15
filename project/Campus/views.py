from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.forms.models import model_to_dict
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
# Create your views here.
from .models import AcademicStaff, Section
from .forms import *
from .models import *
from django.db.models import Q

from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    advisors = AcademicStaff.objects.all()
    sections = Section.objects.all()
    context = {
        "advisors": advisors,
        'sections': sections,
    }

    return render(request, 'home.html', context)

@login_required
def display_students(request, pk=None):
    myid=request.user.id
    advisor = get_object_or_404(AcademicStaff, pk=myid)
    students = advisor.student_set.all()
    context = {
        'students': students,
    }
    return render(request, 'students.html', context)

class SectionUpdateView(UpdateView):
    model = Section
    template_name = 'change_section.html'
    fields = [
        'quota',
    ]

    def get_success_url(self):
        return reverse("home")

@login_required
def special_quota(request):

    staff = Staff.objects.get(user=request.user)
    user = AcademicStaff.objects.get(staff=staff)
    sections = user.section_set.all()
    context = {
        'sections': sections
    }
    return render(request, 'special_quota.html', context)

@login_required
def open_special_quota(request):
    if request.method == 'POST':
        student_number_id = request.POST.get("student_number")
        section_id = request.POST.get("section")
        print(student_number_id, section_id)

        section = get_object_or_404(Section, id=section_id)

        student = get_object_or_404(Student, st_id=student_number_id)
        print("at")
        section.special_quota.add(student)

    return HttpResponseRedirect("/")

@login_required
def harf_notu(request):
    staff = get_object_or_404(Staff, user=request.user)
    user = get_object_or_404(AcademicStaff, staff=staff)
    sections = user.section_set.all()

    context = {
        'sections': sections
    }
    return render(request, 'harf_notu.html', context)

@login_required
def get_section_students(request, pk=None):
    section = get_object_or_404(Section, pk=pk)
    context = {
        'students': section.students.all(),
        'section': section,
    }
    return render(request, 'get_section_students.html', context)

@login_required
def give_note(request):
    if request.method == 'POST':
        grade = request.POST.get("harf_notu")
        st_id = request.POST.get("student_id")
        section_id = request.POST.get("section_id")
        section = get_object_or_404(Section, id=section_id)
        student = get_object_or_404(Student, st_id=st_id)
        ccr_course = get_object_or_404(CcrCourse, ccr=student.curriculum)

        CompletedCourse.objects.create(
            student=student,
            ccr_course=ccr_course,
            act_course=section.course,
            grade=grade
        )

    return HttpResponseRedirect("/")
@login_required
def studentsOfMyCourses(request):
    # VERDİĞİM DERSLERİN ÖĞRENCİLERİ
    url = 'studentsOfMyCourses.html'
    staff = get_object_or_404(Staff, user=request.user)
    user = get_object_or_404(AcademicStaff, staff=staff)
    sections = Section.objects.all()
    myCourses = []

    for section in sections:
        if user == section.instructor:
            myCourses.append(section)

    takenCourses = TakenCourse.objects.all()
    students = []

    for takenCourse in takenCourses:

        for course in myCourses:

            if takenCourse.act_course == course:

                students.append(takenCourse)




    content = {'students' : students}
    return render(request, url, content)
   
@login_required
def myStudents(request):

    url = 'myStudents.html'

    # ADVISORI OLDUGUM OGRENCILER

    # to retrieve all students
    students = []
    students = Student.objects.all()

    # to obtain related students
    related_students = []

    # to visit all students
    for student in students:

        # to obtain advisor and the person (who did request)
        if student.advisor.staff.user.id == request.user.id:

            # to add related student in to the list
            related_students.append(student)

        # otherwise
        else:
            # to redirect to invalid page
            return redirect("/invalid")

    content = {'related_students' : related_students}

    return render(request, url, content)


@login_required
def student_courses(request, pk=None):
    student = get_object_or_404(Student, pk=pk)
    context = {
        'taken_courses': student.takencourse_set.all()
    }
    return render(request, 'student_courses.html', context)
@login_required
def base(request):
    url= 'base.html'
    print("testtt")
    staff = get_object_or_404(Staff, user=request.user)
    user = get_object_or_404(AcademicStaff, staff=staff)
    sections = Section.objects.all()
    myCourses = []

    for section in sections:
        if user == section.instructor:
            myCourses.append(section)


    content = {'myCourses' : myCourses}

    return render(request, url, content)

@login_required
def displayTranscript(request, st_id=None):
    url = 'display-transcript.html'
    student = get_object_or_404(Student, st_id=st_id)
    completedCourses = CompletedCourse.objects.filter(student=student)



    print("hello")

    return render(request, url, {'completedCourses' : completedCourses})
@login_required
def displaySchedule(request, st_id=None):
    url = 'display-schedule.html'

    # ilgili öğrenciyi çekme
    student = get_object_or_404(Student, st_id=st_id)

    # ilgili öğrencinin tüm derslerini takenCourse dan alma
    takenCourses = TakenCourse.objects.filter(student=student)
    sections = []

    # öğrencinin aldığı derslerdeki section bilgilerini yeni bir listede tutma
    for tc in takenCourses:
        sections.append(tc.act_course)

    # tüm scheduleları çekme
    schedules = Schedule.objects.all()
    related_schedules = []

    # tüm schedule lardaki sectionlar ile kendi sectionlarımı karşılaştırıp, ilgili olan scheduleları yeni bir listeye atama
    for sc in schedules:
        for sec in sections:
            if sc.section == sec:
                related_schedules.append(sc)

    content = {'related_schedules' : related_schedules}

    return render(request, url, content)
@login_required
def displayCurriculum(request, st_id=None):
    url = 'display-curriculum.html'
    student = get_object_or_404(Student, st_id=st_id)
    curriculum = CcrCourse.objects.filter(curriculum=student.curriculum)
    content = {'curriculum' : curriculum}
    return render(request, url, content )
@login_required
def displayCCR(request, st_id=None):
    url = 'display-ccr.html'
    student = get_object_or_404(Student, st_id=st_id)
    completedCourses = CompletedCourse.objects.filter(student=student)
    takenCourses = TakenCourse.objects.filter(student=student)
    content = {'completedCourses' : completedCourses, 'takenCourses' : takenCourses}
    return render(request, url, content)
@login_required
def openNewSection(request):

    url = 'open-new-section.html'

    if request.method == 'POST':
        form = OpenNewSection(request.POST)
        if form.is_valid():
            form.save()
            course = form.cleaned_data['course']
            number = form.cleaned_data['number']
            instructor = form.cleaned_data['instructor']
            semester = form.cleaned_data['semester']
        else:
            return redirect('/invalid')
    else:
        form = OpenNewSection()

    return render(request, url, {'form':form})
@login_required
def myCourses(request):

    url = 'my-courses.html'
    staff = get_object_or_404(Staff, user=request.user)
    user = get_object_or_404(AcademicStaff, staff=staff)
    sections = Section.objects.all()
    myCourses = []

    for section in sections:
        if user == section.instructor:
            myCourses.append(section)


    content = {'myCourses' : myCourses}
    return render(request, url, content)
@login_required
def myCourseDetails(request, pk=None):

    url = 'my-course-details.html'
    related_section = get_object_or_404(Section, pk=pk)
    students = TakenCourse.objects.filter(act_course=related_section)
    content = {'students' : students}
    return render(request, url, content)

@login_required
def grade(request, st_id=None, course_id=None):

    url = 'grade.html'
    student = get_object_or_404(Student, st_id=st_id)

    if request.method == 'GET':
        form = Grade2Student()
    else:
        form = Grade2Student(request.POST)
        if form.is_valid():
            completedCourse =CompletedCourse(student=student, grade=form.cleaned_data['grade'])
            completedCourse.save(force_insert=True)
            return redirect('/succesfully')

    return render(request,url,{'form':form})
@login_required
def ScheduleApproveOrReject(request, st_id=None):

    url = 'reject.html'
    student = get_object_or_404(Student, st_id=st_id)
    print(student)

    desiredCourses = TakenCourse.objects.filter(student=student)
    print(desiredCourses)

    for eachCourse in desiredCourses:
        form = ScheduleApproveOrReject(request.GET)
        if form.is_valid():
            form.save()


    return render(request, url, {'form':form})

@login_required
def sectionlar(request):
    url='secitons.html'
    sections = Section.objects.all()
    
    return render(request,url,{'sections': sections})