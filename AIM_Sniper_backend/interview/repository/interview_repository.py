from abc import ABC, abstractmethod


class InterviewRepository(ABC):
    @abstractmethod
    def getMaxId(self):
        pass

    @abstractmethod
    def insertData(self, interviewId, question):
        pass

    @abstractmethod
    def getData(self,sessionId):
        pass