from abc import ABC, abstractmethod


class InterviewService(ABC):
    @abstractmethod
    def insertSession(self):
        pass
    @abstractmethod
    def getSession(self, sessionId):
        pass