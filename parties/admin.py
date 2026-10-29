from django.contrib import admin
from .models import (
    Person,
    StudentEvaluation,
    FeePayment,
    Attendance,
    ChildReport,
    PagePermission,
    ParentStudent,   # أضيفي ده
)

admin.site.register(Person)
admin.site.register(StudentEvaluation)
admin.site.register(FeePayment)
admin.site.register(Attendance)
admin.site.register(ChildReport)
admin.site.register(PagePermission)
admin.site.register(ParentStudent)   # أضيفي ده