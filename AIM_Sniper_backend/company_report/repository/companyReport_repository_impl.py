import os
from company_report.entity.models import CompanyReport
from company_report.repository.companyReport_repository import CompanyReportRepository
from AIM_Sniper_backend import settings
from company_report.repository.data_for_corp_business_repository_impl import DataForCorpBusinessRepositoryImpl
from company_report.repository.data_for_corp_overview_repository_impl import DataForCorpOverviewRepositoryImpl
from company_report.repository.data_for_finance_repository_impl import DataForFinanceRepositoryImpl


class CompanyReportRepositoryImpl(CompanyReportRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__companyBusiness = DataForCorpBusinessRepositoryImpl.getInstance()
            cls.__instance.__companyOverview = DataForCorpOverviewRepositoryImpl.getInstance()
            cls.__instance.__companyFinance = DataForFinanceRepositoryImpl.getInstance()


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

    def extractReportData(self):
        print(f"* CORP_CODE start ----------------")
        corpCodeDict = self.__companyBusiness.getCorpCode()

        print(f"* CORP_OVERVIEW start ----------------")
        corpOverviewRawData = self.__companyOverview.getRawOverviewDataFromDart(corpCodeDict)
        corpOverviewPreprocessedData = self.__companyOverview.preprocessRawData(corpOverviewRawData)

        print(f"* CORP_BUSINESS start ----------------")
        # corpBusinessRawData = self.__companyBusiness.getRawDataFromDart()
        # corpBusinessPreprocessedData = self.__companyBusiness.preprocessRawData(corpBusinessRawData)
        # corpBusinessSummary = self.__companyBusiness.changeContentStyle(corpBusinessPreprocessedData)
        corpBusinessSummary = self.__companyBusiness.changeContentStyle(corpCodeDict)

        print(f"* FINANCIAL_STATEMENTS start ----------------")
        financeProfitDict = self.__companyFinance.getProfitDataFromDart(corpCodeDict)

        return corpOverviewPreprocessedData, corpBusinessSummary, financeProfitDict

    def autoUpdateReport(self):
        companyOverview, companyBusiness, companyFinance = self.extractReportData()
        print(f"{companyOverview}"
              f"{companyBusiness}"
              f"{companyFinance}"
              f"")
