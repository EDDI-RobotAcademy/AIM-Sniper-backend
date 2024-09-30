from abc import ABC, abstractmethod

class CompanyReportService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def createCompanyReport(self, companyReportName, companyReportPrice, companyReportCategory,content, companyReportTitleImage):
        pass

    @abstractmethod
    def readCompanyReport(self, companyReportId):
        pass
    @abstractmethod
    def deleteCompanyReport(self,companyReportId):
        pass

    @abstractmethod
    def updateCompanyReport(self,companyReportId,companyReportData):
        pass
