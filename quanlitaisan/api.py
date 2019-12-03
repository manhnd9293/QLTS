from .models import TaiSan, NhanVien
from django.http import JsonResponse, HttpResponse
import json
import csv
from django.contrib.auth.decorators import login_required

@login_required
def json_detail(request, asset_id):
  # print('id = ' + str(asset_id))
  try:
    asset_id = int(asset_id)
    if request.user.is_superuser:
      obj = TaiSan.objects.filter(pk = asset_id)
      print('got asset from db')
    else:  
      obj = TaiSan.objects.filter(quan_ly__user = request.user,pk = asset_id)
    obj = list(obj)[0]
  except Exception as e:
    print('exception in get json')
    print(e)
    obj = None
  
  if obj:
    obj_dict = obj.__dict__.copy()
    obj_dict.pop('_state')
    obj_dict.pop('ngay_su_dung')
    obj_dict['hien_trang'] = obj.get_hien_trang_display()
    obj_dict['loai_tai_san'] = obj.get_loai_tai_san_display()
    obj_dict['don_vi_tinh'] = obj.get_don_vi_tinh_display()
    print(obj_dict)
    res = json.dumps(obj_dict)
    # print(res)
  else:
    res = json.dumps(None)
  return HttpResponse(res)

@login_required
def search(request, sw):
  obj_list = list(TaiSan.objects.filter(ten_tai_san__icontains = sw))
  res = []
  for obj in obj_list:
    obj_dict = obj.__dict__.copy()
    obj_dict.pop('_state')
    obj_dict.pop('ngay_su_dung')
    obj_dict['hien_trang'] = obj.get_hien_trang_display()
    obj_dict['loai_tai_san'] = obj.get_loai_tai_san_display()
    obj_dict['don_vi_tinh'] = obj.get_don_vi_tinh_display()
    json_obj = json.dumps(obj_dict, ensure_ascii=False)
    res.append(json_obj)
  res = json.dumps(res, ensure_ascii=False)
  # print(res)
  return HttpResponse(res)


class FileExport():
  
  export_data = None
  
  def csv_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="required_item.csv"'
    writer = csv.writer(response)
    meta = TaiSan._meta
    all_fields = [field.name for field in meta.fields]
    all_fields_verbose = [field.verbose_name for field in meta.fields]
    writer.writerow(all_fields_verbose)
    for asset in FileExport.export_data:
      # danh sach thuoc tinh cua tai san
      ls = []
      for field in all_fields:
        ls.append(getattr(asset, field))
      writer.writerow(ls)
    return response
