from survey.entity.survey_title import SurveyTitle
from survey.repository.survey_title_repository import SurveyTitleRepository

class SurveyTitleRepositoryImpl(SurveyTitleRepository):
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

    def registerTitle(self, survey, surveyTitle):
        try:
            SurveyTitle.objects.create(survey_id=survey, title=surveyTitle)
            return True
        except Exception as e:
            print('Title 저장 중 오류 발생 : ', e)
            return False



