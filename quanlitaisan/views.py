from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FormTaiSan, FormBaoTri, FormTimKiemTaiSan
from .models import TaiSan, LichSuBaoTri, NhanVien
from django.core.paginator import Paginator
from .api import FileExport
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

def get_infor_by_user(request):
  user = request.user
  employee = list(NhanVien.objects.filter(user = user))[0]
  assets = TaiSan.objects.filter(quan_ly = employee)
  return {'assets' : assets, 'employee' : employee}

@login_required
def index(req):
  infor = get_infor_by_user(req)
  assets = infor['assets']
  employee = infor['employee']
  if assets.count() > 5: 
    assets = reversed(assets[(len(assets)-5):])
  maintains = LichSuBaoTri.objects.filter(tai_san_bao_tri__quan_ly = employee)
  if maintains.count() > 5:
    maintains = reversed(maintains[(len(maintains)-5):])
  return render(req, 'quanlitaisan/base.html', {'assets': assets,'maintains' : maintains})

@login_required
def details(req, asset_id):
  # obj = TaiSan.objects.get(pk = asset_id)
  obj = get_object_or_404(TaiSan, pk = asset_id)
  child_assets = TaiSan.objects.filter(tai_san_cha  = asset_id)
  history = obj.lichsubaotri_set.all()
  context = {'obj' : obj, 'title': 'Chi tiết','child' : child_assets, 'history' : history}
  return render(req, 'quanlitaisan/detail.html', context)

@login_required
def maintains(request, maintain_id):
  obj = LichSuBaoTri.objects.get(pk = maintain_id)
  return render(request, 'quanlitaisan/maintain_details.html',{'obj': obj, 'title': 'Chi tiết bảo trì'})

@login_required
def assets_list(request, page):
  #add a comment
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  if employee.user.is_superuser:
    assets = TaiSan.objects.filter()
  
  paginator = Paginator(assets, 25)
  title = 'Danh sách tài sản'
  assets = paginator.get_page(page)
  return render(request, 'quanlitaisan/assets_list.html',{'assets': assets, 'title': title})

@login_required
def remove_asset(request, asset_id):
  obj = TaiSan.objects.get(pk = asset_id)
  obj.delete() 
  context = {
        'url_name' : '/assets/1',
        'title' :'Xóa thành công'
      }
  return render(request, 'quanlitaisan/sucess_view.html', context)

@login_required
def search_items(request):
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  
  if request.GET:
    user_criteria = request.GET
    if request.user.is_superuser:
      q = TaiSan.objects.all()
    else:
      q = assets
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

@login_required
def add_asset(request):
  if request.method == 'GET':
    form = FormTaiSan
    context = {
        'title' : 'Thêm tài sản',
        'form' : form
    }
    return render(request, 'quanlitaisan/addItem.html', context)
  else:
    form = FormTaiSan(request.POST)
    if form.is_valid():
      user_data = form.cleaned_data
      new_item = TaiSan(**user_data)
      new_item.save()
      context = {
        'url_name' : '/addItem',
        'title' : 'Lưu tài sản thành công'
      }
      return render(request, 'quanlitaisan/sucess_view.html', context)
    return render(request, 'quanlitaisan/addItem.html', {'title': 'Invalid input', 'form' : form})

@login_required
def add_maintain(request):

  if request.method == 'GET':
    form = FormBaoTri
    return render(request, 'quanlitaisan/addMaintain.html', {'form': form, 'title': 'Thêm bảo trì'})

  else:
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
      return render(request, 'quanlitaisan/addMaintain.html', {'form': form, 'title': 'Invalid input'})

@login_required
def inspect(request):

  if request.method == 'GET':
    return render(request, 'quanlitaisan/kiemke.html',{'title': 'Kiểm kê'})
  
  else:    
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

@login_required
def delete(request, asset_id):
  return render(request, 'quanlitaisan/delete_view.html', {'asset_id': asset_id})

def test(request):
  print('test is called')
  return HttpResponse('done test')

@login_required
def update_asset(request, asset_id):
  if request.method == 'GET':
    asset = TaiSan.objects.get(pk = asset_id)
    form = FormTaiSan(instance= asset)
    return render(request, 'quanlitaisan/update_form.html', {'form': form, 'title': 'Cập nhật thông tin'})
  else:
    asset = TaiSan.objects.get(pk = asset_id)
    update_infor = FormTaiSan(request.POST, instance = asset)
    update_infor.save()
    return render(request, 'quanlitaisan/sucess_view.html', {'title':'Cập nhật thành công', 'url_name': '/search'})
    
def sign_in(request):
  if request.method == 'GET':
    next_url =  request.GET['next']
    return render(request, 'quanlitaisan/signin.html',{})
  else:
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
