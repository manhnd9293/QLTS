from .models import TaiSan
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
      obj = TaiSan.objexts.filter(pk = asset_id)
    else:  
      obj = TaiSan.objects.filter(quan_ly__user = request.user,pk = asset_id)
    obj = list(obj)[0]
  except:
    obj = None
  
  if obj:
    obj_dict = obj.__dict__.copy()
    obj_dict.pop('_state')
    obj_dict.pop('ngay_su_dung')
    obj_dict['hien_trang'] = obj.get_hien_trang_display()
    obj_dict['loai_tai_san'] = obj.get_loai_tai_san_display()
    print(obj_dict)
    res = json.dumps(obj_dict)
  else:
    res = json.dumps(None)
  return HttpResponse(res)

@login_required
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
