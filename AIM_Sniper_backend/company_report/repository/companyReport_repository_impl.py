import os

from django.db.models import Sum

from company_report.entity.company_data_finance import FinancialData
from company_report.entity.company_data_total import CompanyDataTotal
from company_report.entity.models import CompanyReport
from company_report.repository.companyReport_repository import CompanyReportRepository
from AIM_Sniper_backend import settings
from marketing.entity.models import Marketing


class CompanyReportRepositoryImpl(CompanyReportRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return CompanyReport.objects.all().order_by('companyReportName')


    def create(self, companyReportName, companyReportPrice, companyReportCategory, content, companyReportTitleImage):
        uploadDirectory='../../AIM-Sniper-frontend/src/assets/images/uploadimages'
        print('업로드된 디렉토리 : ', uploadDirectory)
        os.makedirs(uploadDirectory, exist_ok=True)

        imagePath = os.path.join(uploadDirectory, companyReportTitleImage.name)
        with open(imagePath, 'wb+') as destination:
            for chunk in companyReportTitleImage.chunks():
                destination.write(chunk)
        print('이미지 경로: ',imagePath)


        companyReport = CompanyReport(
            companyReportName=companyReportName,
            content=content,
            companyReportPrice=companyReportPrice,
            companyReportCategory=companyReportCategory,
            companyReportTitleImage=companyReportTitleImage.name
        )
        companyReport.save()
        return companyReport

    def findByCompanyReportId(self, companyReportId):
        try:
            return CompanyReport.objects.get(companyReportId=companyReportId)
        except CompanyReport.DoesNotExist:
            return None

    def findByCompanyReportIdList(self, companyReportIdList):
        try:
            return CompanyReport.objects.filter(companyReportId__in=companyReportIdList)
        except CompanyReport.DoesNotExist:
            return None

    def findAllByCompanyReportCategory(self, companyReportCategory):
        try:
            return CompanyReport.objects.filter(companyReportCategory=companyReportCategory)
        except:
            return None

    def deleteByCompanyReportId(self, companyReportId):
        companyReport = CompanyReport.objects.get(companyReportId=companyReportId)
        companyReport.delete()

    def update(self, companyReport, companyReportData):
        for key, value in companyReportData.items():
            setattr(companyReport, key, value)
        companyReport.save()
        return companyReport

    def readCompanyReportFinance(self, companyReportName):
        # 해당 회사와 연도의 데이터를 필터링
        id=CompanyDataTotal.objects.get(company_name=companyReportName)
        FinanceData2021 = FinancialData.objects.filter(company=id, year=2021).values('revenue', 'receivable_turnover','operating_cash_flow')
        FinanceData2022 = FinancialData.objects.filter(company=id, year=2022).values('revenue', 'receivable_turnover',
                                                                                    'operating_cash_flow')
        FinanceData2023 = FinancialData.objects.filter(company=id, year=2023).values('revenue', 'receivable_turnover',
                                                                                    'operating_cash_flow')
        # 결과 반환
        return list(FinanceData2021),list(FinanceData2022),list(FinanceData2023)

    def readCompanyReportInfo(self,companyReportName):
        companyReportInfo = CompanyDataTotal.objects.filter(company_name=companyReportName)
        basicInfo=companyReportInfo.values('company_name','est_date','company_class','ceo_name','address','website')
        return basicInfo

    def readCompanyReportSummary(self, companyReportName):
        companyReportSummary = CompanyDataTotal.objects.filter(company_name=companyReportName).values('business_summary')
        return companyReportSummary[0]['business_summary']

    def readTopNCompany(self, topN):
        # companyReport = CompanyReport.objects.all()
        sortedCompany = Marketing.objects.values('product').annotate(Sum('click_count')).order_by('-click_count__sum')
        clickedTopNCompany = [dict['product']
                                for dict in sortedCompany[:topN].values('product')]

        return clickedTopNCompany
