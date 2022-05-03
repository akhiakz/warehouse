from django.contrib import admin
from django.urls import path,re_path
from base_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
    # path('user_logout/', views.user_logout, name='user_logout'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('signup/', views.signup, name='signup'),
    path('signuppage/', views.signuppage, name='signuppage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('sendmail', views.sendmail, name="sendmail"),
    path('requests/', views.requests, name='requests'),
    path('requests_send/', views.requests_send, name='requests_send'),
    path('status/', views.status, name='status'),
    path('order_confirmation/<int:id>', views.order_confirmation, name='order_confirmation'),
    path('confirm_order/<int:id>', views.confirm_order, name='confirm_order'),
    path('orders/', views.orders, name='orders'),
    path('Air_service/', views.Air_service, name='Air_service'),
    path('Ship_service/', views.Ship_service, name='Ship_service'),
    path('Ground_service/', views.Ground_service, name='Ground_service'),
    path('Warehousing/', views.Warehousing, name='Warehousing'),


#############   Admin module ################

    path('Admin_index/', views.Admin_index, name='Admin_index'),
    path('Admin_dashboard/', views.Admin_dashboard, name='Admin_dashboard'),
    path('Admin_requests/', views.Admin_requests, name='Admin_requests'),
    path('request_accept/<int:id>', views.request_accept, name='request_accept'),
    path('request_reject/<int:id>', views.request_reject, name='request_reject'),
    path('Admin_neworder_dptcard/', views.Admin_neworder_dptcard, name='Admin_neworder_dptcard'),
    path('Admin_air_new_orders/', views.Admin_air_new_orders, name='Admin_air_new_orders'),
    path('staff_assign_air/<int:id>', views.staff_assign_air, name='staff_assign_air'),
    path('Admin_ship_new_orders/', views.Admin_ship_new_orders, name='Admin_ship_new_orders'),
    path('staff_assign_ship/<int:id>', views.staff_assign_ship, name='staff_assign_ship'),
    path('Admin_ground_new_orders/', views.Admin_ground_new_orders, name='Admin_ground_new_orders'),
    path('staff_assign_ground/<int:id>', views.staff_assign_ground, name='staff_assign_ground'),
    path('Admin_statics/', views.Admin_statics, name='Admin_statics'),
    path('Admin_accepted_orders/', views.Admin_accepted_orders, name='Admin_accepted_orders'),
    path('Admin_rejected_orders/', views.Admin_rejected_orders, name='Admin_rejected_orders'),
    path('Admin_Staffs/', views.Admin_Staffs, name='Admin_Staffs'),
    path('Admin_addstaff/', views.Admin_addstaff, name='Admin_addstaff'),
    path('add_staff_save/', views.add_staff_save, name='add_staff_save'),
    path('Admin_all_staffs/', views.Admin_all_staffs, name='Admin_all_staffs'),
    path('staff_delete/<int:id>', views.staff_delete, name='staff_delete'),
    path('Admin_contact/', views.Admin_contact, name='Admin_contact'),
    path('Admin_departments/', views.Admin_departments, name='Admin_departments'),
    path('Admin_create_departments/', views.Admin_create_departments, name='Admin_create_departments'),
    path('dpt_save/', views.dpt_save, name='dpt_save'),


#############   Admin module ends ################


#############   Staff module ################

    path('Staff_index/', views.Staff_index, name='Staff_index'),
    path('Staff_account_settings/', views.Staff_account_settings, name='Staff_account_settings'),
    path('staff_acc_save/<int:id>', views.staff_acc_save, name='staff_acc_save'),
    path('Staff_dashboard/', views.Staff_dashboard, name='Staff_dashboard'),
    path('Staff_orders/', views.Staff_orders, name='Staff_orders'),
    path('Staff_completed_orders/', views.Staff_completed_orders, name='Staff_completed_orders'),
    path('Staff_tracking_update/<int:id>', views.Staff_tracking_update, name='Staff_tracking_update'),
    path('Staff_tracking_update_save/<int:id>', views.Staff_tracking_update_save, name='Staff_tracking_update_save'),

#############   Staff module ends ################
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

