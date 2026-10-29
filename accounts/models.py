from django.db import models
from django.contrib.auth.models import User
from django.db import models
import random
import string

# ================================
# 👤 الطالب
# ================================
class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")
    grade = models.IntegerField(default=0, verbose_name="الصف الدراسي")
    student_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="كود الطالب"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
                        
    # ✅ أضف هذا السطر الجديد (تحت سطر user)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    
    
    def save(self, *args, **kwargs):
     if not self.student_code:
        while True:
            code = "ST" + "".join(random.choices(string.digits, k=4))
            if not Student.objects.filter(student_code=code).exists():
                self.student_code = code
                break
     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"
        ordering = ["name"]   # ✅ الطلاب يظهروا بالترتيب الأبجدي للاسم

# ================================
#ولي الامر
# ================================
class Parent(models.Model):
    parent_name = models.CharField(max_length=100, verbose_name="اسم ولي الأمر")
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")

    def __str__(self):
        return self.parent_name

    class Meta:
        verbose_name = "ولي أمر"
        verbose_name_plural = "أولياء الأمور"
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
    related_name="account_fee_payments",
)

    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="المبلغ")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الدفع")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash', verbose_name="طريقة الدفع")

    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم عملية التحويل")
    sender_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف المحول منه")
    receipt_image = models.ImageField(upload_to='payments/receipts/', blank=True, null=True, verbose_name="صورة الإيصال")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="حالة الدفع")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم المسجل", null=True, blank=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = "عملية دفع"
        verbose_name_plural = "عمليات الدفع"

    def __str__(self):
        student_name = self.student.user.username if self.student and self.student.user else "طالب غير محدد"
        user_name = self.user.username if self.user else "غير محدد"
        return f"{student_name} - {self.amount} ج.م - {user_name}"


# ================================
# 📊 التقييمات
# ================================
class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المعلمة")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ التقييم")

    MOOD_CHOICES = [
        ('happy', 'سعيد'),
        ('sad', 'حزين'),
        ('tired', 'مرهق'),
        ('sick', 'مريض'),
        ('sleeping', 'نائم'),
    ]
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, verbose_name="حالة الطفل", default='happy')

    SUBJECT_CHOICES = [
    ("english", "English"),
    ("math", "Math"),
    ("science", "Science"),
    ("prewriting", "Pre Writing"),
    ("religion", "دين"),
    ("arabic", "لغة عربية"),
    ("skills", "تنمية مهارات"),
    ("online", "أونلاين"),
    ("drawing", "رسم"),
    ("other", "أخرى"),
            ]

    
    subject = models.CharField(
       max_length=30,
       choices=SUBJECT_CHOICES,
       blank=True,
       null=True,
        )

    RESPONSE_CHOICES = [
        ('good', 'جيد'),
        ('average', 'متوسط'),
        ('weak', 'ضعيف'),
    ]
    response = models.CharField(max_length=20, choices=RESPONSE_CHOICES, verbose_name="الاستجابة", default='average')

    BEHAVIOR_CHOICES = [
        ('obedient', 'مطيع'),
        ('disobedient', 'غير مطيع'),
        ('hyperactive', 'كثير الحركة'),
    ]
    behavior = models.CharField(max_length=20, choices=BEHAVIOR_CHOICES, verbose_name="السلوك", default='obedient')

    bathroom_from = models.TimeField(null=True, blank=True, verbose_name="من وقت الحمام")
    bathroom_to = models.TimeField(null=True, blank=True, verbose_name="إلى وقت الحمام")
    sleep_from = models.TimeField(null=True, blank=True, verbose_name="من وقت النوم")
    sleep_to = models.TimeField(null=True, blank=True, verbose_name="إلى وقت النوم")

    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات المعلمة")

    def __str__(self):
        return f"{self.student.name} - {self.date}"

class Expense(models.Model):
    description = models.CharField(max_length=200, verbose_name="وصف المصروف")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ المصروف")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    class Meta:
        ordering = ["-date"]
        verbose_name = "مصروف"
        verbose_name_plural = "المصروفات"

    def __str__(self):
        return f"{self.description} - {self.amount} ج.م"

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("admin", "مدير"),
        ("teacher", "معلم"),
        ("parent", "ولي أمر"),
        ("student", "طالب"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
