from survey.entity.survey_question import SurveyQuestion
from survey.repository.survey_question_repository import SurveyQuestionRepository

class SurveyQuestionRepositoryImpl(SurveyQuestionRepository):
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

    def registerQuestion(self, survey, questionTitle, questionType, essential):
        try:
            SurveyQuestion.objects.create(survey_id=survey, question=questionTitle,
                                          question_type=questionType, essential=essential)
            return True

        except Exception as e:
            print('Question 저장 중 오류 발생 : ', e)
            return False