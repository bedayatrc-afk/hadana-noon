from django.urls import path
from . import views

print("========== ACCOUNTS URLS LOADED ==========")
urlpatterns = [

    # ─── الصفحة الرئيسية ───────────────────────────────
    path('', views.landing_page, name='landing_page'),

    # ─── تسجيل الدخول والخروج ──────────────────────────
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    # ─── الداشبوردات ───────────────────────────────────
    path('main-dashboard/', views.main_dashboard, name='main_dashboard'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),

    # ─── التسجيلات ─────────────────────────────────────
    path('register-student/', views.register_student, name='register_student'),
    path('register-parent/', views.register_parent, name='register_parent'),
    path('register-user/', views.register_user, name='register_user'),
    path('link-student/', views.link_student, name='link_student'),

    # ─── التقييمات ─────────────────────────────────────
    path('evaluation/', views.evaluation, name='evaluation'),
    path('evaluations-list/', views.evaluations_list, name='evaluations_list'),
    path('evaluation/print/<int:id>/', views.print_evaluation, name='print_evaluation'),
    path('evaluation/send-mail/<int:id>/', views.send_evaluation_mail, name='send_evaluation_mail'),
    path('export-evaluations/', views.export_evaluations_excel, name='export_evaluations_excel'),

    # ─── المدفوعات ─────────────────────────────────────
    path("pay-fees/", views.pay_fees, name="pay_fees"),
    path('payments-list/', views.payments_list, name='payments_list'),
    path('payment/print/<int:id>/', views.print_payment, name='print_payment'),
    path('export-payments/', views.export_payments_excel, name='export_payments'),

    # ─── الحضور والغياب ────────────────────────────────
    path('attendance/add/', views.add_attendance, name='add_attendance'),

    # ─── المصاريف والتقارير والإعدادات ─────────────────
    path('expenses/', views.expenses, name='expenses'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings_page, name='settings'),

    # ─── Autocomplete ──────────────────────────────────
    path('autocomplete/student/', views.student_autocomplete, name='student_autocomplete'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('attendance/export/', views.export_attendance_excel, name='export_attendance_excel'),

    # ─── Student Code Search ────────────────────────────
    path('student-code/', views.student_code_search, name='student_code_search'),

    path('test-url/', views.landing_page, name='test_url'),
]

