from abc import ABC, abstractmethod


class SurveySelectionRepository(ABC):
    @abstractmethod
    def registerSelection(self, question, selection):
        pass

    @abstractmethod
    def getSelectionsByQuestionId(self, questionId):
        pass

    @abstractmethod
    def findSelection(self, selectionId):
        pass