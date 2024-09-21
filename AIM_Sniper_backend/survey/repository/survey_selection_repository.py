from abc import ABC, abstractmethod


class SurveySelectionRepository(ABC):
    @abstractmethod
    def registerSelection(self, question, selection):
        pass