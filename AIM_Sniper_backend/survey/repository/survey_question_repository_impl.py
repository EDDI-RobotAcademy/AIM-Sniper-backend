import os

from survey.entity.survey_image import SurveyImage
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

    def registerQuestion(self, survey, questionTitle, questionType, essential, images):
        try:
            SurveyQuestion.objects.create(survey_id=survey, question=questionTitle,
                                          question_type=questionType, essential=essential)
            questionId = SurveyQuestion.objects.get(survey_id=survey, question=questionTitle, question_type=questionType, essential=essential)
            if len(images) !=0:
                for image in images:
                    SurveyImage.objects.create(question_id=questionId, image=image.name)
                    uploadDirectory = '..\\..\\AIM-Sniper-frontend\\src\\assets\\images\\uploadimages'
                    imagePath = os.path.join(uploadDirectory, image.name)
                    with open(imagePath, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    print('이미지 경로: ', imagePath)

            return questionId.id

        except Exception as e:
            print('Question 저장 중 오류 발생 : ', e)
            return False

    def findQuestion(self, questionId):
        question = SurveyQuestion.objects.get(id=questionId)
        return question

    def getQuestionsBySurveyId(self, surveyId):
        questions = SurveyQuestion.objects.filter(survey_id=surveyId)
        questionList = questions.order_by('id').values_list('id', 'question', 'question_type', 'essential')
        images = []
        for question in questions:
            questionImage = SurveyImage.objects.filter(question_id=question).order_by('id').values_list('question_id', 'image')
            images.append(questionImage)

        questionImageList = [img for img in images[0]]
        print('questionImageList: ', questionImageList)

        questionList = list(questionList)
        for i, q in enumerate(questionList) :
            if q[2] == 'checkbox':
                questionList[i] = {'questionId': q[0], 'questionTitle': q[1], 'questionType': q[2], 'essential': q[3],
                                   'answer': [], 'images': [image for qId, image in questionImageList if qId == q[0]]}
            else :
                questionList[i] = {'questionId': q[0], 'questionTitle': q[1], 'questionType': q[2], 'essential': q[3],
                                   'answer': '', 'images': [image for qId, image in questionImageList if qId == q[0]]}
        return questionList



