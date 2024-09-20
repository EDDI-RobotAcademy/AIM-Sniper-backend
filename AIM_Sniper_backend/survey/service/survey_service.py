from abc import ABC, abstractmethod


class SurveyService(ABC):
    @abstractmethod
    def createSurveyForm(self):
        pass


