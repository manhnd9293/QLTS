from django import forms
from django.forms import ModelForm
from .models import TaiSan, LichSuBaoTri 

forms.DateInput.input_type = 'date'


class FormTaiSan(ModelForm):
  class Meta:
    model = TaiSan
    fields = '__all__'
    widgets = {
        'ngay_su_dung': forms.DateInput()
    }


class FormTimKiemTaiSan(ModelForm):
  class Meta:
    model = TaiSan
    fields = ('loai_tai_san', 'ten_tai_san')


class FormBaoTri(ModelForm):
  class Meta:
    model = LichSuBaoTri
    fields = '__all__'