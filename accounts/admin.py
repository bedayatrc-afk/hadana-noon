from django.contrib import admin
from django.utils.html import format_html
from .models import Student, FeePayment, Evaluation, Parent
from .models import UserProfile

# 👤 الطالب
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'grade', 'user')   # ✅ اسم الطالب ظاهر هنا
    search_fields = ('name', 'user__username')                # بحث بالاسم أو اسم المستخدم
    list_filter = ('grade',)                                  # ف فلترة حسب الصف الدراسي
#parent
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "parent_name", "phone")

# 💰 دفع الرسوم
@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_method', 'status', 'payment_date', 'view_receipt')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('student__user__username', 'transaction_id', 'sender_phone')
    readonly_fields = ('payment_date',)

    def view_receipt(self, obj):
        if obj.receipt_image:
            return format_html('<a href="{}" target="_blank">عرض الصورة</a>', obj.receipt_image.url)
        return "لا توجد صورة"

    view_receipt.short_description = "صورة الإيصال"


# 📊 التقييمات
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'mood', 'subject', 'response', 'behavior', 'teacher')
    list_filter = ('mood', 'subject', 'response', 'behavior', 'date')
    search_fields = ('student__user__username', 'notes', 'teacher__username')
    readonly_fields = ('date',)

admin.site.register(UserProfile)