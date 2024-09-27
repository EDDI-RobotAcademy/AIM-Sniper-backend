from abc import ABC, abstractmethod


class SurveySelectionRepository(ABC):
    @abstractmethod
    def registerSelection(self, question, selection):
        pass

    @abstractmethod
    def getSelectionsByQuestionId(self, questionId):
        pass

    @abstractmethod
    def findSelectionBySelectionId(self, selection):
        pass

    @abstractmethod
    def findSelectionBySelectionName(self, selectionName):
        pass