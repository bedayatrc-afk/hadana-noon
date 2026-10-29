from django import forms
from .models import StudentEvaluation, FeePayment, Attendance
from accounts.models import Student


def student_queryset():
    return Student.objects.all().order_by("name")


class StudentEvaluationForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=student_queryset())

    class Meta:
        model = StudentEvaluation
        fields = [
            "student",
            "mood",
            "subject",
            "response",
            "attendance",
            "behavior",
            "level",
            "bathroom_from",
            "bathroom_to",
            "sleep_from",
            "sleep_to",
            "notes",
        ]


class FeePaymentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=student_queryset())

    class Meta:
        model = FeePayment
        fields = ['student', 'amount', 'notes']


class AttendanceForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=student_queryset())

    class Meta:
        model = Attendance
        fields = "__all__"