from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .forms import AttendanceForm, FeePaymentForm, StudentEvaluationForm
from .models import ChildReport, Person, Attendance, FeePayment
from permissions_app.decorators import role_required
from .models import Person


def home(request):
    return render(request, 'home.html')

@login_required
@role_required("admin", "teacher")
def parties_home(request):
    attendance_form = AttendanceForm()
    payment_form = FeePaymentForm()
    evaluation_form = StudentEvaluationForm()
    
    all_attendance = Attendance.objects.all().order_by('-id')
    all_payments = FeePayment.objects.all().order_by('-id')
    all_reports = ChildReport.objects.all().order_by('-id')
    
    return render(request, 'parties/parties.html', {
        'attendance_form': attendance_form,
        'payment_form': payment_form,
        'evaluation_form': evaluation_form,
        'all_attendance': all_attendance,
        'all_payments': all_payments,
        'all_reports': all_reports,
    })

@login_required
@role_required("admin", "teacher")
@csrf_protect
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parties_home')
    else:
        form = AttendanceForm()
            
    return render(request, 'add_attendance.html', {'form': form})

@login_required
@role_required("admin")
@csrf_protect
def add_payment(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('payment_list_view')
        else:
            print(form.errors)   # أضف هذا السطر

    else:
        form = FeePaymentForm()

    return render(request, 'add_payment.html', {'form': form})


@login_required
@role_required("admin", "teacher")
@csrf_protect
def add_evaluation(request):
    if request.method == 'POST':
        form = StudentEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parties_home')
        else:
             print(form.errors)    
    
    else:
        form = StudentEvaluationForm()

    return render(request, 'add_evaluation.html', {'form': form})

@login_required
@role_required("admin", "teacher")
@csrf_protect
def add_child_report(request):
    persons = Person.objects.filter(role="student").order_by("name")

    if request.method == "POST":
        student_id = (request.POST.get("student_id") or "").strip()
        student = persons.filter(pk=student_id).first() if student_id.isdigit() else None
        date_raw = (request.POST.get("date_time") or "").strip()
        if not student:
            return render(request, "parties/child_report.html", {
                "persons": persons,
                "error": "اختر طالبًا مسجلًا من القائمة، ولا تكتب اسمًا غير موجود.",
            })
        try:
            parsed_date = datetime.fromisoformat(date_raw)
            if timezone.is_naive(parsed_date):
                parsed_date = timezone.make_aware(parsed_date, timezone.get_current_timezone())
        except (TypeError, ValueError):
            return render(request, "parties/child_report.html", {
                "persons": persons,
                "error": "أدخل تاريخًا ووقتًا صحيحين.",
            })

        report = ChildReport.objects.create(
            student=student,
            date_time=parsed_date,
            child_status=(request.POST.get("child_status") or "").strip(),
            study=(request.POST.get("study") or "").strip(),
            response_level=(request.POST.get("response_level") or "").strip(),
            behavior_level=(request.POST.get("behavior_level") or "").strip(),
            bath_from=request.POST.get("bath_from") or None,
            bath_to=request.POST.get("bath_to") or None,
            sleep_from=request.POST.get("sleep_from") or None,
            sleep_to=request.POST.get("sleep_to") or None,
            teacher_note=(request.POST.get("teacher_note") or "").strip(),
        )
        messages.success(request, "تم حفظ تقرير الطفل بنجاح.")
        return redirect("child_reports_list")

    return render(request, "parties/child_report.html", {"persons": persons})

@login_required
@role_required("admin", "teacher")
def child_reports_list(request):
    reports = ChildReport.objects.all().order_by('-id')
    return render(request, "parties/child_reports_list.html", {
        "reports": reports
    })

@login_required
@role_required("admin")
def payment_list_view(request):
    payments = FeePayment.objects.all().order_by('-id')
    return render(request, 'parties/payment_list.html', {
        'payments': payments
    })
