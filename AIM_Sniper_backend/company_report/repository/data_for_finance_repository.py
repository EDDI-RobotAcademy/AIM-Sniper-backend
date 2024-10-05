from abc import ABC, abstractmethod


class DataForFinanceRepository(ABC):
    @abstractmethod
    def preprocessFSFromDart(self, *dfs):
        pass

    @abstractmethod
    def selectIncomeDocument(self, parsedData):
        pass

    @abstractmethod
    def getFinancialStatements(self, corpCode):
        pass

    @abstractmethod
    def checkLabelNameInFS(self, df, *probableNames):
        pass

    @abstractmethod
    def checkLabelComboNameInFS(self, df, *comboNames):
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