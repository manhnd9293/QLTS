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
  maintains = LichSuBaoTri.objects.filter(tai_san_bao_tri__quan_ly = employee)
  return {'assets' : assets, 'employee' : employee, 'maintains': maintains}

@login_required
def index(req):
  if req.user.is_superuser:
    assets = TaiSan.objects.all()
    maintains = LichSuBaoTri.objects.all()
    employee = list(NhanVien.objects.filter(user = req.user))[0]
  else:
    infor = get_infor_by_user(req)
    assets = infor['assets']
    maintains = infor['maintains']
    employee = infor['employee']

  # get last 5 assets and maintain
  if assets.count() > 5: 
    assets = reversed(assets[(len(assets)-5):])
  if maintains.count() > 5:
    maintains = reversed(maintains[(len(maintains)-5):]) 
  return render(req, 'quanlitaisan/base.html', {'assets': assets,'maintains' : maintains, 'title': 'Trang chủ', 'name': employee.name})

@login_required
def index_update(request):
  return render(request, 'quanlitaisan/index1.html')

@login_required
def details(req, asset_id):
  # obj = TaiSan.objects.get(pk = asset_id)
  infor = get_infor_by_user(req)
  assets = infor['assets']
  employee = infor['employee']
  obj = get_object_or_404(TaiSan, pk = asset_id)
  child_assets = TaiSan.objects.filter(tai_san_cha  = asset_id)
  history = obj.lichsubaotri_set.all()
  context = {'obj' : obj, 'title': 'Chi tiết','child' : child_assets, 'history' : history, 'name' : employee.name}
  return render(req, 'quanlitaisan/detail.html', context)

@login_required
def maintains(request, maintain_id):
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  obj = LichSuBaoTri.objects.get(pk = maintain_id)
  return render(request, 'quanlitaisan/maintain_details.html',{'obj': obj, 'title': 'Chi tiết bảo trì','name' : employee.name})

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
  return render(request, 'quanlitaisan/assets_list.html',{'assets': assets, 'title': title, 'name': employee.name})

@login_required
def remove_asset(request, asset_id):
  if not request.user.is_superuser:
    return HttpResponse('Access denied')
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  obj = TaiSan.objects.get(pk = asset_id)
  obj.delete() 
  context = {
        'url_name' : '/assets/1',
        'title' :'Xóa thành công',
        'name' : employee.name
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

    return render(request, 'quanlitaisan/resultpage.html', {'obj': q, 'title': 'Kết quả tìm kiếm', 'name': employee.name})
  else:
    return render(request, 'quanlitaisan/search.html', { 'title': 'Tìm kiếm tài sản', 'name': employee.name})

@login_required
def add_asset(request):
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  if request.method == 'GET':
    form = FormTaiSan
    context = {
        'title' : 'Thêm tài sản',
        'form' : form,
        'name' : employee.name
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
        'title' : 'Lưu tài sản thành công',
        'name' : employee.name
      }
      return render(request, 'quanlitaisan/sucess_view.html', context)
    return render(request, 'quanlitaisan/addItem.html', {'title': 'Invalid input', 'form' : form})

@login_required
def add_maintain(request):
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']

  if request.method == 'GET':
    form = FormBaoTri
    return render(request, 'quanlitaisan/addMaintain.html', {'form': form, 'title': 'Thêm bảo trì','name' : employee.name})

  else:
    form = FormBaoTri(request.POST)
    if form.is_valid():
      user_data = form.cleaned_data
      new_item = LichSuBaoTri(**user_data)
      new_item.save()

      context = {
        'url_name' : '/addMaintain',
        'title': 'Thêm thành công',
        'name' : employee.name
      }
      return render(request, 'quanlitaisan/sucess_view.html', context)
    else:
      return render(request, 'quanlitaisan/addMaintain.html', {'form': form, 'title': 'Invalid input'})

@login_required
def inspect(request):
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  if request.method == 'GET':
    return render(request, 'quanlitaisan/kiemke.html',{'title': 'Kiểm kê','name' : employee.name})
  
  else:    
    update_infor = request.POST
    assets = update_infor.getlist('id')
    states = update_infor.getlist('quantity')
    
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
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  if not request.user.is_superuser:
    return HttpResponse('Access denied')
  return render(request, 'quanlitaisan/delete_view.html', {'asset_id': asset_id, 'name': employee.name})

@login_required
def update_asset(request, asset_id):
  infor = get_infor_by_user(request)
  assets = infor['assets']
  employee = infor['employee']
  if not request.user.is_superuser:
    return HttpResponse('Access denied')

  if request.method == 'GET':
    asset = TaiSan.objects.get(pk = asset_id)
    form = FormTaiSan(instance= asset)
    return render(request, 'quanlitaisan/update_form.html', {'form': form, 'title': 'Cập nhật thông tin'})
  else:
    asset = TaiSan.objects.get(pk = asset_id)
    update_infor = FormTaiSan(request.POST, instance = asset)
    update_infor.save()
    return render(request, 'quanlitaisan/sucess_view.html', {'title':'Cập nhật thành công', 'url_name': '/search'})

@login_required      
def nhap_hang(request):
  return render(request, 'quanlitaisan/nhaphang.html', {'title': 'Nhập hàng'})

@login_required
def display_profile(request):
  infor = get_infor_by_user(request)
  ast = infor['assets']
  emp = infor['employee']
  return render(request, 'quanlitaisan/profile.html', {'title': 'Thông tin cá nhân', 'emp' : emp})


def sign_in(request):
  if request.method == 'GET':
    next_url =  request.GET['next']
    return render(request, 'quanlitaisan/signin.html', {'title': 'Đăng nhập'})
  else:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      return render(request, 'quanlitaisan/signin.html', 
      {'error_mess': 'Sai thông tin người dùng hoặc mật khẩu. Vui lòng nhập lại'})
 
def signout(request):
  logout(request)
  return redirect('/')

  
