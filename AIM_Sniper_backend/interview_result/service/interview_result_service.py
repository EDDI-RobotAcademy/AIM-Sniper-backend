from abc import ABC, abstractmethod

class InterviewResultService(ABC):
    @abstractmethod
    def saveInterviewResult(self, scoreResultList, accountId):
        pass


    @abstractmethod
    def getInterviewResult(self, accountId):
        pass
