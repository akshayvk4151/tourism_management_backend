from django.urls import path
from . import views

app_name = 'admin_app'


urlpatterns = [
   
    path('dashboard/',views.dashboard),
    path('admin_name/<int:name_id>/',views.admin_name),
    path('view_customer/',views.view_customer),
    path('delete_customer/<int:id>/',views.delete_customer),
    path('add_blog/',views.add_blog),
    path('adminView_blog/',views.adminView_blog),
    path('update_blog/<int:id>/',views.update_blog),
    path('delete_blog/<int:id>/',views.delete_blog),
    path('add_destination/',views.add_destination),
    path('view_destination/',views.view_destination),
    path('delete_destination/<int:id>/',views.delete_destination),
    path('edit_destination/<int:destination_id>/',views.edit_destination),
    path('view_queries/',views.view_queries),
    path('delete_queries/<int:query_id>/',views.delete_queries),
    path('change_password/',views.change_password),
    path('admin_logout/',views.admin_logout),

]
