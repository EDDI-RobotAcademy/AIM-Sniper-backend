from survey.entity.survey_selection import SurveySelection
from survey.repository.survey_selection_repository import SurveySelectionRepository


class SurveySelectionRepositoryImpl(SurveySelectionRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def registerSelection(self, question, selection):
        try:
            SurveySelection.objects.create(survey_question_id=question, selection=selection)
            serveySelection = SurveySelection.objects.get(survey_question_id=question, selection=selection)

            return serveySelection.id

        except Exception as e:
            print('Selection 저장 중 오류 발생 : ', e)