from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.parties_home, name='parties_home'),

    path('add-evaluation/', views.add_evaluation, name='add_evaluation'),

    # أضفنا السلاش / في آخر الرابط هنا عشان يطابق الـ redirect المريح في الـ view
    path('add-payment/', views.add_payment, name='add_payment'),

    path('add-attendance/', views.add_attendance, name='add_attendance'),

    # 🆕 تقرير الطفل اليومي
    path('add-child-report/', views.add_child_report, name='add_child_report'),

    # 🆕 عرض كل التقارير
    path('child-reports/', views.child_reports_list, name='child_reports_list'),

    # 🆕 السطر الجديد: لعرض جدول الفلوس والمدفوعات المستقل
    path('payments-list/', views.payment_list_view, name='payment_list_view'),
    path(
        'settings/password/', 
        auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), 
        name='password_change'
    ),
    path(
        'settings/password/done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), 
        name='password_change_done'
    ),
]