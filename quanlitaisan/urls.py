from django.urls import path, re_path
from . import views, api

app_name = 'quanlitaisan'

urlpatterns = [
  path('', views.index, name = 'index'),
  path('details/<int:asset_id>', views.details, name = 'details'),
  path('maintain/<int:maintain_id>', views.maintains, name = 'maintains'),
  path('search/', views.SearchView.as_view(), name = 'search'),
  path('addItem/', views.AddAssetView.as_view(), name = 'add_item'),
  path('addMaintain/', views.AddMaintain.as_view(), name = 'add_maintain'),
  path('assets/<int:page>', views.assets_list, name = 'assets_list'),
  path('about/', views.MyView.as_view(), name = 'test'),
  path('remove/<int:asset_id>', views.remove_asset, name = 'remove_asset'),
  path('kiemke', views.Inspect.as_view(), name = 'kiemke'),
  path('api/<str:asset_id>', api.json_detail, name = 'json_details'),
  path('api/export/', api.FileExport.csv_export, name = 'csv'),
  path('delete/<int:asset_id>', views.delete, name = 'delete_view'),
  path('signout', views.signout, name = 'signout_view'),
  path('accounts/login/', views.SignIn.as_view())
  # path('test', views.test, name= 'test'),
]