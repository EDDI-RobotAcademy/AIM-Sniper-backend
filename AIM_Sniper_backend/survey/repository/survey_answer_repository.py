from abc import ABC, abstractmethod


class SurveyAnswerRepository(ABC):

    @abstractmethod
    def saveTextAnswer(self, question, answer, account):
        pass

    @abstractmethod
    def saveRadioAnswer(self, question, selectionId, account):
        pass

    @abstractmethod
    def saveCheckboxAnswer(self, question, selectionIdArray, account):
        pass

    @abstractmethod
    def getTextAnswersByQuestionId(self, questionId):
        pass

    @abstractmethod
    def getSelectionAnswersByQuestionId(self, questionId):
        pass

    @abstractmethod
    def getAnswerByAccountId(self, accountId):
        pass
