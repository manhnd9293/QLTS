from django.urls import path, re_path
from . import views

app_name = 'quanlitaisan'

urlpatterns = [
  path('', views.index, name = 'index'),
  path('details/<int:asset_id>', views.details, name = 'details'),
  path('maintain/<int:maintain_id>', views.maintains, name = 'maintains'),
  path('search/', views.SearchView.as_view(), name = 'search'),
  path('addItem/', views.AddAssetView.as_view(), name = 'add_item'),
  path('addMaintain/', views.add_maintain, name = 'add_maintain'),
  path('assets/<int:page>', views.assets_list, name = 'assets_list'),
  path('about/', views.MyView.as_view(), name = 'test')
]