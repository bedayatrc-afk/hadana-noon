from django.db import models
from django.contrib.auth.models import User
from accounts.models import Student
from django.utils import timezone
from accounts.models import Student

# ================================
# 👤 الأشخاص (طلاب / مدرسين / أولياء أمور)
# ================================
class Person(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ROLE_CHOICES = [
        ('student', 'طالب'),
        ('teacher', 'مدرس'),
        ('parent', 'ولي أمر'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    national_id = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

# ================================
# 📊 تقييم الطلاب
# ================================
class StudentEvaluation(models.Model):

    MOOD_CHOICES = [
        ("happy", "😊 سعيد"),
        ("normal", "😐 عادي"),
        ("sad", "😢 حزين"),
    ]

    RESPONSE_CHOICES = [
        ("excellent", "ممتاز"),
        ("good", "جيد"),
        ("average", "متوسط"),
        ("weak", "ضعيف"),
    ]

    SUBJECT_CHOICES = [
        ("math", "رياضيات"),
        ("physics", "فيزياء"),
        ("chemistry", "كيمياء"),
        ("english", "إنجليزي"),
        ("history", "تاريخ"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="الطالب"
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        blank=True,
        null=True
    )

    subject = models.CharField(
        max_length=30,
        choices=SUBJECT_CHOICES,
        blank=True,
        null=True
    )

    response = models.CharField(
        max_length=20,
        choices=RESPONSE_CHOICES,
        blank=True,
        null=True
    )

    behavior = models.IntegerField(default=0)
    attendance = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    bathroom_from = models.TimeField(blank=True, null=True)
    bathroom_to = models.TimeField(blank=True, null=True)

    sleep_from = models.TimeField(blank=True, null=True)
    sleep_to = models.TimeField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"تقييم {self.student.name}"



# ================================
# 💰 دفع الرسوم
# ================================
class FeePayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'كاش يدوي'),
        ('vf_cash', 'فودافون كاش'),
        ('bank', 'تحويل بنكي'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'قيد المراجعة'),
        ('confirmed', 'تم التأكيد'),
        ('rejected', 'مرفوض'),
    ]

    student = models.ForeignKey(
    Student,
    on_delete=models.CASCADE,
    related_name="party_fee_payments",
)

    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="المبلغ")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الدفع")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash', verbose_name="طريقة الدفع")

    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم عملية التحويل")
    sender_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف المحول منه")
    receipt_image = models.ImageField(upload_to='payments/receipts/', blank=True, null=True, verbose_name="صورة إيصال التحويل")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="حالة الدفع")

    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    def __str__(self):
        return f"{self.student.name} - {self.amount} ج.م - {self.get_status_display()}"


# ================================
# 🕒 الحضور والانصراف
# ================================
class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="الطالب"
    )
    date = models.DateField(null=True, blank=True, verbose_name="التاريخ")
    status = models.CharField(
        max_length=20,
        choices=[
            ('present', 'حضور'),
            ('absent', 'غياب'),
        ],
        verbose_name="الحالة"
    )

    def __str__(self):
        return f"{self.student.name} - {self.get_status_display()}"


# ================================
# 🆕 تقرير الطفل اليومي
# ================================
class ChildReport(models.Model):
    student = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        verbose_name="الطالب"
    )
    date_time = models.DateTimeField(verbose_name="التاريخ والوقت")
    child_status = models.CharField(max_length=20, verbose_name="حالة الطفل")
    study = models.CharField(max_length=50, blank=True, verbose_name="الدراسة")
    response_level = models.CharField(max_length=30, blank=True, verbose_name="مستوى الاستجابة")
    behavior_level = models.CharField(max_length=30, blank=True, verbose_name="مستوى السلوك")
    bath_from = models.TimeField(null=True, blank=True, verbose_name="من وقت الحمام")
    bath_to = models.TimeField(null=True, blank=True, verbose_name="إلى وقت الحمام")
    sleep_from = models.TimeField(null=True, blank=True, verbose_name="من وقت النوم")
    sleep_to = models.TimeField(null=True, blank=True, verbose_name="إلى وقت النوم")
    teacher_note = models.TextField(blank=True, verbose_name="ملاحظات المعلمة")

    def __str__(self):
        return f"{self.student.name} - {self.date_time.strftime('%d/%m/%Y %H:%M')}"
    

class PagePermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    students = models.BooleanField(default=False)
    attendance = models.BooleanField(default=False)
    evaluation = models.BooleanField(default=False)
    payments = models.BooleanField(default=False)
    reports = models.BooleanField(default=False)
    settings = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class ParentStudent(models.Model):

    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="children"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="parents"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.parent.username} - {self.student.name}"