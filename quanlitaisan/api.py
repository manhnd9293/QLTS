from .models import TaiSan
from django.http import JsonResponse, HttpResponse
import json
import csv


def json_detail(request, asset_id):
  print('id = ' + str(asset_id))
  try:
    asset_id = int(asset_id)
    obj = TaiSan.objects.get(pk = asset_id)
  except:
    obj = None
  if obj:
    obj_dict = obj.__dict__.copy()
    obj_dict.pop('_state')
    obj_dict.pop('ngay_su_dung')
    res = json.dumps(obj_dict)
  else:
    res = json.dumps(None)
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
