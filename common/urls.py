from django.urls import path
from . import views

app_name = 'common'


urlpatterns = [
    path('destination_index/',views.destination_index),
    path('customer_register/',views.customer_register),
    path('customer_login/',views.customer_login),
    path('customer_accound/<int:customer_id>/',views.customer_accound),
    path('view_profile/<int:customer_id>/',views.view_profile),
    path('edit_profile/<int:customer_id>/',views.edit_profile),
    
    path('blog/',views.blog),
    path('view_blog/<int:post_id>/',views.view_blog, name='view_blog'),
    path('view_destinations/<int:destination_id>/',views.view_destinations, name='view_destinations'),
    path('book_destination/<int:destination_id>/<int:customer_id>/', views.book_destination),



    path('change_password/',views.change_password),
    path('contact_us/',views.contact_us),
    path('customer_logout/', views.customer_logout, name='customer_logout'),


    path('admin_register/',views.admin_register),
    path('admin_login/',views.admin_login),

    
]
