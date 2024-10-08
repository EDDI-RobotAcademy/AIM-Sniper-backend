from django.db import models
from company_report.entity.company_data_total import CompanyDataTotal


class FinancialData(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyDataTotal, on_delete=models.CASCADE)
    year = models.IntegerField()
    revenue = models.BigIntegerField() #재무 지표 매출액
    receivable_turnover = models.FloatField()  #매출 채권 회전율
    operating_cash_flow = models.BigIntegerField() #영업 활동 현금 흐름

    def __str__(self):
        return f"({self.year})"

    class Meta:
        db_table = 'company_finance'
        app_label = 'company_report'