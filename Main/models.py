from django.db import models

# Create your models here.
class DataEntry(models.Model):
    unix_month = models.IntegerField()
    parameter_a = models.FloatField()
    parameter_b = models.FloatField()
    parameter_c = models.FloatField()
    parameter_d = models.FloatField()
    parameter_e = models.FloatField()
    parameter_f = models.FloatField()
    parameter_g = models.FloatField()
    parameter_h = models.FloatField()

    @property
    def converted_date(self):
        # 將UNIX月份轉換成西元年月
        year = 1970 + self.unix_month // 12
        month = self.unix_month % 12 + 1
        return f"{year}-{month:02d}"
