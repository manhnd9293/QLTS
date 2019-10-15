from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FormTaiSan, FormBaoTri, FormTimKiemTaiSan
from .models import TaiSan, LichSuBaoTri
from django.core.paginator import Paginator

def index(req):
  assets = TaiSan.objects.all()
  if assets.count() > 5: 
    assets = reversed(assets[(len(assets)-5):])
  maintains = LichSuBaoTri.objects.all()
  if maintains.count() > 5:
    maintains = reversed(maintains[(len(maintains)-5):])
  print(maintains)
  return render(req, 'quanlitaisan/index.html', {'assets': assets,'maintains' : maintains})

def details(req, asset_id):
  obj = TaiSan.objects.get(pk = asset_id)
  child_assets = TaiSan.objects.filter(tai_san_cha  = asset_id)
  history = obj.lichsubaotri_set.all()
  context = {'obj' : obj, 'title': 'Chi tiết','child' : child_assets, 'history' : history}
  return render(req, 'quanlitaisan/detail.html', context)

def maintains(request, maintain_id):
  obj = LichSuBaoTri.objects.get(pk = maintain_id)
  return render(request, 'quanlitaisan/maintain_details.html',{'obj': obj, 'title': 'Chi tiết bảo trì'})

def assets_list(request, page):
  #add a comment
  assets_all = TaiSan.objects.all()
  paginator = Paginator(assets_all, 25)
  title = 'Danh sách tài sản'
  assets = paginator.get_page(page)
  return render(request, 'quanlitaisan/assets_list.html',{'assets': assets, 'title': title})

def remove_asset(request, asset_id):
  obj = TaiSan.objects.get(pk = asset_id)
  obj.delete() 
  context = {
        'url_name' : '/assets/1',
        'title' :'Xóa thành công'
      }
  return render(request, 'quanlitaisan/sucess_view.html', context)

import csv

def csv_export(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="allItem.csv"'
  writer = csv.writer(response)
  q = TaiSan.objects.all()
  meta = TaiSan._meta
  all_fields = [field.name for field in meta.fields]
  print(all_fields)
  writer.writerow(all_fields)
  for ast in q:
    data = []
    for f in all_fields:
      data.append(getattr(ast, f))
    writer.writerow(data)
  return response

from django.views import View

class MyView(View):
  def get(self, request):
    return render(request, 'quanlitaisan/base.html', {'title' : 'About us'})

class SearchView(View):
  def get(self, request):
    if request.GET:
      q = TaiSan.objects
      id = request.GET.get('asset_id')
      
      if id:
        q = q.filter(id = id)
      loai_ts = request.GET.get('loai_tai_san')
      
      if loai_ts:
        q = q.filter(loai_tai_san = loai_ts)
      
      ten_ts = request.GET.get('ten_tai_san')  
      if ten_ts:
        q = q.filter(ten_tai_san__icontains = ten_ts)
      return render(request, 'quanlitaisan/resultpage.html', {'obj': q, 'title': 'Kết quả tìm kiếm'})
    else:
      return render(request, 'quanlitaisan/search.html', { 'title': 'Tìm kiếm tài sản'})


class AddAssetView(View):
  form_class = FormTaiSan
  template_name = 'quanlitaisan/addItem.html'
  
  def get(self, request):
    form = self.form_class()
    context = {
        'title' : 'Thêm tài sản',
        'form' : form
    }
    return render(request, self.template_name, context)
  
  def post(self, request):
    form = self.form_class(request.POST)
    print(request.POST)
    if form.is_valid():
      user_data = form.cleaned_data
      new_item = TaiSan(**user_data)
      new_item.save()
      context = {
        'url_name' : '/addItem',
        'title' : 'Lưu tài sản thành công'
      }
      return render(request, 'quanlitaisan/sucess_view.html', context)
    return render(request, self.template_name, {'title': 'Invalid input', 'form' : form})

class AddMaintain(View):
  form_class = FormBaoTri
  template_name = 'quanlitaisan/addMaintain.html'
  
  def get(self, request):
    form = self.form_class()
    return render(request, self.template_name , {'form': form, 'title': 'Thêm bảo trì'})

  def post(self, request):
    form = FormBaoTri(request.POST)
    if form.is_valid():
      user_data = form.cleaned_data
      new_item = LichSuBaoTri(**user_data)
      new_item.save()

      context = {
        'url_name' : '/addMaintain',
        'title': 'Thêm thành công'
      }
      return render(request, 'quanlitaisan/sucess_view.html', context)
    else:
      return render(request, self.template_name, {'form': form, 'title': 'Invalid input'})

class Inspect(View):
  def get(self, request):
    return render(request, 'quanlitaisan/kiemke.html',{})
  
  def post(self, request):
    context = {
      'url_name' : '/kiemke',
      'title' : 'Lưu tài sản thành công'
    }
    infor = request.POST
    print(infor)
    return render(request, 'quanlitaisan/sucess_view.html', context)


