from .models import TaiSan
from django.http import JsonResponse, HttpResponse
import json


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