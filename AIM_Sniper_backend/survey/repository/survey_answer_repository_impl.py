from survey.entity.survey_answer import SurveyAnswer
from survey.repository.survey_answer_repository import SurveyAnswerRepository

class SurveyAnswerRepositoryImpl(SurveyAnswerRepository):
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

    def saveTextAnswer(self,  question, answer):
        try:
            SurveyAnswer.objects.create(survey_question_id=question, answer=answer)
            return True
        except Exception as e :
            print('text answer 저장 과정에서 오류 발생! : ', e)
            return False

    def saveRadioAnswer(self, question, selectionId):
        try:
            SurveyAnswer.objects.create(survey_question_id=question, survey_selection_id=selectionId)
            return True
        except Exception as e :
            print('radio answer 저장 과정에서 오류 발생! : ', e)
            return False


    def saveCheckboxAnswer(self, question, selectionIdArray):
        try:
            for selectionId in selectionIdArray:
                SurveyAnswer.objects.create(survey_question_id=question, survey_selection_id=selectionId)
            return True
        except Exception as e :
            print('checkbox answer 저장 과정에서 오류 발생!: ', e)
            return False


