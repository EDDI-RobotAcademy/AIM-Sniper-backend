from abc import ABC, abstractmethod


class SurveyService(ABC):
    @abstractmethod
    def createSurveyForm(self):
        pass
    @abstractmethod
    def getSurveyBySurveyId(self, surveyId):
        pass

    @abstractmethod
    def getQuestionByQuestionId(self, questionId):
        pass

    @abstractmethod
    def registerTitleDescription(self, survey, surveyTitle, surveyDescription):
        pass

    @abstractmethod
    def registerQuestion(self, survey, questionTitle, questionType, essential):
        pass

    @abstractmethod
    def registerSelection(self, question, selection):
        pass

    @abstractmethod
    def getSurveyList(self):
        pass

    @abstractmethod
    def registerAnswer(self):
        pass
