from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Phong(models.Model):
  DEFAULT_PK = 1
  ten_phong = models.CharField('Tên phòng', max_length = 30)

  def __str__(self):
    ten_hien_thi = 'id :' + str(self.id) + '---'+ 'name: ' + self.ten_phong
    return ten_hien_thi
 
class NhanVien(models.Model):
  user = models.OneToOneField(User, on_delete= models.CASCADE)
  ten = models.CharField('Họ và tên', max_length = 40)
  phong = models.ForeignKey(Phong, on_delete= models.SET_NULL, null = True, blank = True, verbose_name = 'Phòng')

class QuanLy(models.Model):
  phong = models.ForeignKey(Phong, on_delete= models.CASCADE, verbose_name = 'Phòng')
  nhan_vien = models.ForeignKey(NhanVien, on_delete= models.SET_NULL,null = True, blank = True, verbose_name = 'Nhân viên quản lý')


class TaiSan(models.Model):
  LOAI_TAI_SAN = [
    ('VT', 'Vật tư'),
    ('TB', 'Thiết bị')
  ]

  HIEN_TRANG = [
    ('SD', 'Đang sử dụng'),
    ('BH', 'Bị hỏng'),
  ]
  
  loai_tai_san       = models.CharField('loại tài sản', max_length = 2, choices = LOAI_TAI_SAN)
  ten_tai_san        = models.CharField('tên tài sản', max_length = 20)
  ngay_su_dung       = models.DateField('ngày bắt đầu sử dụng')
  thoi_han_bao_hanh  = models.PositiveIntegerField('số năm bảo hành')
  thoi_gian_sd       = models.PositiveIntegerField('số năm sử dụng')
  tai_san_cha        = models.ForeignKey('self', on_delete = models.SET_NULL, null = True, blank = True,verbose_name = 'Thiết bị chứa')
  dia_diem           = models.ForeignKey(Phong, on_delete=models.SET_DEFAULT, default = Phong.DEFAULT_PK)
  hien_trang         = models.CharField('Hiện trạng', max_length = 2, choices = HIEN_TRANG)
  phu_trach          = models.ForeignKey(NhanVien, on_delete= models.SET_NULL, null = True, blank = True, verbose_name = 'Người phụ trách')
  
  def __str__(self):
    ten_hien_thi = 'id :' + str(self.id) + '---'+ 'name: ' + self.ten_tai_san
    return ten_hien_thi
 
 
class LichSuBaoTri(models.Model):
  ngay_bao_tri    = models.DateField('Ngày Bảo Trì')
  tai_san_bao_tri = models.ForeignKey(TaiSan, on_delete = models.CASCADE, verbose_name = 'Tài sản bảo trì')
  tieu_de         = models.CharField('Tiêu đề', max_length = 30)
  noi_dung        = models.TextField('Nội dung bảo trì')

  def __str__(self):
    return str(self.tai_san_bao_tri)

