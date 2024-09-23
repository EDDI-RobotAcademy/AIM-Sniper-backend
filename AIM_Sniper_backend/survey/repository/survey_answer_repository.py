from abc import ABC, abstractmethod


class SurveyAnswerRepository(ABC):

    @abstractmethod
    def saveTextAnswer(self, question, answer):
        pass

    @abstractmethod
    def saveRadioAnswer(self, question, selectionId):
        pass

    @abstractmethod
    def saveCheckboxAnswer(self, question, selectionIdArray):
        pass
