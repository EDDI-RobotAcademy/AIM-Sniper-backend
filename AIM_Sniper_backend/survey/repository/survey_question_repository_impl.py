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
            questionId = SurveyQuestion.objects.get(survey_id=survey, question=questionTitle)
            return questionId.id

        except Exception as e:
            print('Question 저장 중 오류 발생 : ', e)
            return False

    def findQuestion(self, questionId):
        question = SurveyQuestion.objects.get(id=questionId)
        return question

    def getQuestionsBySurveyId(self, surveyId):
        questions = SurveyQuestion.objects.filter(survey_id=surveyId).order_by('id').values_list('id', 'question', 'question_type', 'essential')
        questions = list(questions)
        for i, q in enumerate(questions) :
            questions[i] = {'questionId': q[0], 'questionTitle': q[1], 'questionType': q[2], 'essential': q[3]}

        return questions



