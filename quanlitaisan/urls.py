from django.urls import path, re_path
from . import views, api

app_name = 'quanlitaisan'

urlpatterns = [
  # path('', views.index, name = 'index'),
  path('', views.index_update, name = 'index_update'),
  path('details/<int:asset_id>', views.details, name = 'details'),
  path('maintain/<int:maintain_id>', views.maintains, name = 'maintains'),
  path('search/', views.search_items, name = 'search'),
  path('addItem/', views.add_asset, name = 'add_item'),
  path('addMaintain/', views.add_maintain, name = 'add_maintain'),
  path('assets/<int:page>', views.assets_list, name = 'assets_list'),
  path('remove/<int:asset_id>', views.remove_asset, name = 'remove_asset'),
  path('kiemke', views.inspect, name = 'kiemke'),
  path('api/<str:asset_id>', api.json_detail, name = 'json_details'),
  path('api/search/<str:sw>', api.search, name = 'json_search'),
  path('api/export/', api.FileExport.csv_export, name = 'csv'),
  path('delete/<int:asset_id>', views.delete, name = 'delete_view'),
  path('signout', views.signout, name = 'signout_view'),
  path('accounts/login/', views.sign_in, name = 'sign_in_view'),
  path('assets/update/<int:asset_id>', views.update_asset, name = 'update'),
  path('nhap/', views.nhap_hang, name = 'nhap_hang'),
  path('profile/', views.display_profile, name = 'profile')
  # path('test', views.test, name= 'test'),
]