from django import forms
from .models import FeePayment, Student, Evaluation, Expense

# ✅ فورم دفع الرسوم
class FeePaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ عرض كل الطلاب في القائمة المنسدلة
        self.fields['student'].queryset = Student.objects.all()

        if 'payment_date' in self.fields:
            self.fields['payment_date'].disabled = True

    class Meta:
        model = FeePayment
        fields = [
            'student',
            'amount',
            'notes',
            'payment_method',
            'transaction_id',
            'sender_phone',
            'receipt_image',
            'status'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'w-full border p-3 rounded-lg'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full border p-3 rounded-lg'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full border p-3 rounded-lg'}),
            'payment_method': forms.Select(attrs={'class': 'w-full border p-3 rounded-lg'}),
            'transaction_id': forms.TextInput(attrs={'class': 'w-full border p-3 rounded-lg'}),
            'sender_phone': forms.TextInput(attrs={'class': 'w-full border p-3 rounded-lg'}),
            'receipt_image': forms.ClearableFileInput(attrs={'class': 'w-full border p-3 rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full border p-3 rounded-lg'}),
        }


class EvaluationForm(forms.ModelForm): 
    student = forms.ModelChoiceField(
    queryset=Student.objects.select_related("user").all(),
    empty_label="اختر الطالب",   # ✅ ده يمنع ظهور "طالب جديد"
    label="👦 الطالب",
    widget=forms.Select(attrs={'class': 'w-full border p-3 rounded-lg'})
)


    class Meta: 
        model = Evaluation
        fields = [
            "student", "mood", "subject", "response", "behavior",
            "bathroom_from", "bathroom_to", "sleep_from", "sleep_to", "notes"
        ]
        widgets = {
            'mood': forms.RadioSelect,
            'subject': forms.RadioSelect,
            'response': forms.RadioSelect,
            'behavior': forms.RadioSelect,
            'bathroom_from': forms.TimeInput(attrs={'type': 'time'}),
            'bathroom_to': forms.TimeInput(attrs={'type': 'time'}),
            'sleep_from': forms.TimeInput(attrs={'type': 'time'}),
            'sleep_to': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "amount", "notes"]
        widgets = {
            "description": forms.TextInput(attrs={"placeholder": "مثال: أدوات تعليمية", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "placeholder": "0.00", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "ملاحظات اختيارية", "class": "form-control"}),
        }
