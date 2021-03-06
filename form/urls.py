from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('get_detail/', views.get_detail, name='get_detail'),
    path('save_resp/', views.save_resp, name='save_resp'),
    path('save_title/', views.save_title, name='save_title'),

    path('get_status/', views.get_status, name='get_status'),
    path('get_resp_count/', views.get_resp_count, name='get_resp_count'),
    path('remake/', views.remake, name='remake'),
    path('remove/', views.remove, name='remove'),

    path('get_form_resps/', views.get_form_resps, name='get_form_resps'),
    path('get_form_stats/', views.get_form_stats, name='get_form_stats'),
    path('get_form_resp_full_details/', views.get_form_resp_full_details, name='get_form_resp_full_details'),
    path('get_resp_detail/', views.get_resp_detail, name='get_resp_detail'),
    path('remove_resp/', views.remove_resp, name='remove_resp'),

    path('get_form_settings/', views.get_form_settings, name='get_form_settings'),
    path('save_form_settings/', views.save_form_settings, name='save_form_settings'),

    path('get_overview/', views.get_overview, name='get_overview'),
    path('get_folder_overview/', views.get_folder_overview, name='get_folder_overview'),
    path('get_folder_all/', views.get_folder_all, name='get_folder_all'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('rename_folder/', views.rename_folder, name='rename_folder'),
    path('remove_folder/', views.remove_folder, name='remove_folder'),
    path('move_to_folder/', views.move_to_folder, name='move_to_folder'),
    path('copy/', views.copy, name='copy'),

    path('get_org_overview/', views.get_org_overview, name='get_org_overview'),
    path('get_org_folders/', views.get_org_folders, name='get_org_folders'),
]
