from django.db import models

class CompanyReport(models.Model):
    companyReportId = models.AutoField(primary_key=True)
    companyReportName = models.CharField(max_length=128, null=False)
    companyReportPrice = models.IntegerField(null=False)
    companyReportCategory = models.CharField(max_length=10, null=False)
    content = models.TextField()
    companyReportTitleImage = models.CharField(max_length=100) # 이미지 경로가 들어간다
    # 추후 이미지 관련 필드 추가
    regDate = models.DateTimeField(auto_now_add=True)
    updDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.companyReportName

    class Meta:
        db_table = 'company_report'
        app_label = 'company_report'