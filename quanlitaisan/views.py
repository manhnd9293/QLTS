from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FormTaiSan, FormBaoTri, FormTimKiemTaiSan
from .models import TaiSan, LichSuBaoTri
from django.core.paginator import Paginator


def index(req):
  assets = TaiSan.objects.all()
  assets = reversed(assets[(len(assets)-5):])
  maintains = LichSuBaoTri.objects.all()
  maintains = reversed(maintains[(len(maintains)-5):])
  print(maintains)
  return render(req, 'quanlitaisan/index.html', {'assets': assets,'maintains' : maintains})

def details(req, asset_id):
  obj = TaiSan.objects.get(pk = asset_id)
  child_assets = TaiSan.objects.filter(tai_san_cha  = asset_id)
  history = obj.lichsubaotri_set.all()
  context = {'obj' : obj, 'title': 'Chi tiết','child' : child_assets, 'history' : history}
  return render(req, 'quanlitaisan/detail.html', context)


def search_view(request):
  form = FormTimKiemTaiSan(request.GET)
  if form.is_valid():
    user_data = form.cleaned_data
    print(user_data)
    q = TaiSan.objects

    id = request.GET.get('asset_id')
    if id:
      q = q.filter(id = id)

    loai_ts = user_data.get('loai_tai_san')
    q = q.filter(loai_tai_san = loai_ts)

    ten_ts = user_data.get('ten_tai_san')  
    q = q.filter(ten_tai_san__icontains = ten_ts)
    return render(request, 'quanlitaisan/resultpage.html', {'obj': q, 'title': 'Kết quả tìm kiếm'})
  else:
    form = FormTimKiemTaiSan()
    return render(request, 'quanlitaisan/search.html', {'form' : form, 'title': 'Tìm kiếm tài sản'})


def add_item(request):
  if request.method == 'POST':
      form = FormTaiSan(request.POST)
      if form.is_valid():
        user_data = form.cleaned_data
        new_item = TaiSan(**user_data)
        new_item.save()

        context = {
          'url_name' : '/addItem',
          'title' : 'Lưu thành công'
        }
        return render(request, 'quanlitaisan/sucess_view.html', context)
  else:
      form = FormTaiSan()
  return render(request, 'quanlitaisan/addItem.html', {'form': form, 'title' : 'Thêm tài sản'})

def add_maintain(request):
  if request.method == 'POST':
    form = FormBaoTri(request.POST)
    if form.is_valid():
      user_data = form.cleaned_data
      new_item = LichSuBaoTri(**user_data)
      new_item.save()

      context = {
        'url_name' : '/addMaintain',
        'title' : 'Thêm thành công'
      }
      return render(request, 'quanlitaisan/sucess_view.html', context)
  else:
    form = FormBaoTri()

  return render(request, 'quanlitaisan/addMaintain.html', {'form': form, 'title': 'Thêm bảo trì'})

def maintains(request, maintain_id):
  obj = LichSuBaoTri.objects.get(pk = maintain_id)
  return render(request, 'quanlitaisan/maintain_details.html',{'obj': obj, 'title': 'Chi tiết bảo trì'})

def assets_list(request, page):
  assets_all = TaiSan.objects.all()
  paginator = Paginator(assets_all, 25)
  # page = request.GET.get('page')
  # page = 1
  title = 'Danh sách tài sản'
  assets = paginator.get_page(page)
  return render(request, 'quanlitaisan/assets_list.html',{'assets': assets, 'title': title})
