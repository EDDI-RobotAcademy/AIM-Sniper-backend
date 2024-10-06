from abc import ABC, abstractmethod


class DataForFinanceRepository(ABC):
    @abstractmethod
    def selectIncomeDocument(self, parsedData):

        pass

    @abstractmethod
    def parsingFromOpenAPI(self, corpCode):

        pass

    @abstractmethod
    def getFinancialStatements(self, parsedData, financialStatementsType):

        pass

    @abstractmethod
    def checkLabelNameInFS(self, dfIndex, *probableNames):

        pass

    @abstractmethod
    def checkLabelComboNameInFS(self, dfIndex, *comboNames):

        pass

    @abstractmethod
    def getRevenueTrend(self, income):

        pass

    @abstractmethod
    def getReceivableTurnover(self, income, balance):

        pass

    @abstractmethod
    def getOperatingCashFlow(self, cashFlow):

        pass

    @abstractmethod
    def getProfitDataFromDart(self, corpCodeDict):

        pass