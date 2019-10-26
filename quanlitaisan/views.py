from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FormTaiSan, FormBaoTri, FormTimKiemTaiSan
from .models import TaiSan, LichSuBaoTri
from django.core.paginator import Paginator
from .api import FileExport
from django.contrib.auth import authenticate, login, logout


def index(req):
  assets = TaiSan.objects.all()
  if assets.count() > 5: 
    assets = reversed(assets[(len(assets)-5):])
  maintains = LichSuBaoTri.objects.all()
  if maintains.count() > 5:
    maintains = reversed(maintains[(len(maintains)-5):])
  return render(req, 'quanlitaisan/base.html', {'assets': assets,'maintains' : maintains, 'title': 'Trang chủ'})

def details(req, asset_id):
  # obj = TaiSan.objects.get(pk = asset_id)
  obj = get_object_or_404(TaiSan, pk = asset_id)
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



from django.views import View

class MyView(View):
  def get(self, request):
    return render(request, 'quanlitaisan/test.html', {'title' : 'About us'})

class SearchView(View):
  def get(self, request):
    if request.GET:
      # print(request.GET)
      user_criteria = request.GET
      
      q = TaiSan.objects.all()
      id = user_criteria.get('asset_id')
      loai_ts = user_criteria.get('loai_tai_san')
      ten_ts = user_criteria.get('ten_tai_san')  
      from_date = user_criteria.get('from_date')
      to_date = user_criteria.get('to_date')
      hien_trang_sd = user_criteria.get('hien_trang')
      if id:
        q = q.filter(id = id)
      if loai_ts:
        q = q.filter(loai_tai_san = loai_ts)
      if ten_ts:
        q = q.filter(ten_tai_san__icontains = ten_ts)
      if from_date:
        q = q.filter(ngay_su_dung__gte = from_date)
      if to_date:
        q = q.filter(ngay_su_dung__lte = to_date)
      if hien_trang_sd:
        q = q.filter(hien_trang = hien_trang_sd)

      FileExport.export_data = q

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
    return render(request, 'quanlitaisan/kiemke.html',{'title': 'Kiểm kê'})
  
  def post(self, request):
    
    update_infor = request.POST
    assets = update_infor.getlist('id')
    states = update_infor.getlist('state')
    
    success_item = 0
    failed_item = 0
    error_list = []
    for (id, state) in zip(assets, states):
      id = int(id)
      try:    
        asset = TaiSan.objects.get(pk = id)
        success_item +=1
      except:
        asset = None
        failed_item += 1
        error_list.append(id)
        # pass
      if asset:
        asset.hien_trang = state
        asset.save()
    context = {
      'url_name' : '/kiemke',
      'title' : 'Lưu dữ liệu thành công',
      'sucess' : success_item,
      'fail' : failed_item,
      'error_list': error_list
    }
    return render(request, 'quanlitaisan/update_sucess.html', context)

def delete(request, asset_id):
  return render(request, 'quanlitaisan/delete_view.html', {'asset_id': asset_id})

def test(request):
  print('test is called')
  return HttpResponse('done test')

class SignIn(View):
  def get(self, request):
    return render(request, 'quanlitaisan/signin.html',{})
  
  def post(self, request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      return render(request, 'quanlitaisan/base.html', 
      {'error_mess': 'Sai thông tin người dùng hoặc mật khẩu. Vui lòng nhập lại'})

def signout(request):
  logout(request)
  return redirect('/')