import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_platform.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Student, UserProfile

print("🔄 بدء إضافة البيانات الوهمية الشاملة...")

# 1. إنشاء ولي أمر
parent_user, _ = User.objects.get_or_create(
    username='parent1',
    defaults={'email': 'parent@test.com', 'first_name': 'أحمد', 'last_name': 'ولي الأمر'}
)
parent_user.set_password('123456')
parent_user.save()

profile, _ = UserProfile.objects.get_or_create(user=parent_user)
profile.role = 'parent'
profile.save()

# 2. إنشاء طالب
student_user, _ = User.objects.get_or_create(
    username='student1',
    defaults={'email': 'student@test.com', 'first_name': 'محمد', 'last_name': 'أحمد'}
)
student_user.set_password('123456')
student_user.save()

student, created = Student.objects.get_or_create(
    user=student_user,
    defaults={
        'name': 'محمد أحمد',
        'grade': 3,
        'phone': '01012345678',
        'parent': parent_user  # ✅ ربط مباشر من البداية للتجربة
    }
)
print(f"✅ تم إعداد الطالب: {student.name} (كود: {student.student_code})")

# ---------------------------------------------------------
# 3. إضافة بيانات وهمية للتقييمات والحضور والمصاريف
# ملاحظة: إذا كانت أسماء النماذج مختلفة في مشروعك، عدّل الأسماء أدناه
# ---------------------------------------------------------

try:
    from accounts.models import Evaluation, Attendance, FeePayment
    
    # إضافة تقييمات وهمية
    emojis = ['😊', '😐', '😢', '🌟']
    days = ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء']
    for i, day in enumerate(days):
        Evaluation.objects.get_or_create(
            student=student,
            day=day,
            defaults={'emoji': random.choice(emojis), 'notes': 'أداء جيد'}
        )
    print("✅ تمت إضافة التقييمات اليومية.")

    # إضافة سجل حضور وهمي
    Attendance.objects.get_or_create(
        student=student,
        date=datetime.now().date(),
        defaults={'status': 'present', 'notes': 'حاضر في الموعد'}
    )
    print("✅ تمت إضافة سجل الحضور.")

    # إضافة مصاريف وهمية
    FeePayment.objects.get_or_create(
        student=student,
        description='مصروفات شهر أكتوبر',
        defaults={'amount': 500, 'status': 'paid', 'date': datetime.now().date()}
    )
    print("✅ تمت إضافة بيانات المصاريف.")

except ImportError:
    print("⚠️ تنبيه: لم يتم العثور على نماذج (Evaluation, Attendance, FeePayment).")
    print("   سيتم عرض اللوحة بدون بيانات تفصيلية حتى يتم إنشاء هذه النماذج في models.py")

print("🎉 انتهت عملية إضافة البيانات الوهمية بنجاح!")