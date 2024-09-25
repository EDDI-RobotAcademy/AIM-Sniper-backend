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

    # if accountId is not None:
    #     accountId = self.__accountRepository.findById(accountId)
    #     self.__surveyAnswerRepository.saveAccountId(accountId)
    def saveTextAnswer(self,  question, answer, account):
        try:
            if account is not None:
                SurveyAnswer.objects.create(survey_question_id=question, answer=answer, account=account)
            else:
                SurveyAnswer.objects.create(survey_question_id=question, answer=answer)
            return True
        except Exception as e :
            print('text answer 저장 과정에서 오류 발생! : ', e)
            return False

    def saveRadioAnswer(self, question, selectionId, account):
        try:
            if account is not None:
                SurveyAnswer.objects.create(survey_question_id=question, survey_selection_id=selectionId, account=account)
            else:
                SurveyAnswer.objects.create(survey_question_id=question, survey_selection_id=selectionId)
            return True
        except Exception as e :
            print('radio answer 저장 과정에서 오류 발생! : ', e)
            return False


    def saveCheckboxAnswer(self, question, selectionIdArray, account):
        try:
            for selectionId in selectionIdArray:
                if account is not None:
                    SurveyAnswer.objects.create(survey_question_id=question, survey_selection_id=selectionId, account=account)
                else:
                    SurveyAnswer.objects.create(survey_question_id=question, survey_selection_id=selectionId)
            return True
        except Exception as e :
            print('checkbox answer 저장 과정에서 오류 발생!: ', e)
            return False


