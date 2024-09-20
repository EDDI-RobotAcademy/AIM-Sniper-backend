from abc import ABC, abstractmethod

class SurveyQuestionRepository(ABC):
    @abstractmethod
    def registerQuestion(self, survey, questionTitle, questionType, essential):
        pass