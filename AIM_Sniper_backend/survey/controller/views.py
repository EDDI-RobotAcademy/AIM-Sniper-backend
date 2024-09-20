from rest_framework import viewsets, status
from rest_framework.response import Response
from survey.service.survey_service_impl import SurveyServiceImpl

class SurveyView(viewsets.ViewSet):
    surveyService = SurveyServiceImpl.getInstance()

    def createSurveyForm(self, request):
        surveyId = self.surveyService.createSurveyForm()
        return Response(surveyId, status=status.HTTP_200_OK)

    def registerTitleDescription(self, request):
        surveyId = request.data.get('surveyId')
        surveyTitle = request.data.get('surveyTitle')
        surveyDescription = request.data.get('surveyDescription')
        print(f'surveyId : {surveyId}, surveyTitle: {surveyTitle}, surveyDescription: {surveyDescription}')

        survey = self.surveyService.getSurveyBySurveyId(surveyId)
        result = self.surveyService.registerTitleDescription(survey, surveyTitle, surveyDescription)
        return Response(result, status=status.HTTP_200_OK)


    def registerQuestion(self, request):
        surveyId = request.data.get('surveyId')
        questionTitle = request.data.get('questionTitle')
        questionType = request.data.get('questionType')
        essential = request.data.get('isEssential')
        survey = self.surveyService.getSurveyBySurveyId(surveyId)
        result = self.surveyService.registerQuestion(survey, questionTitle, questionType, essential)
        return Response(result, status=status.HTTP_200_OK)


    def registerSelection(self, request):
        pass
    def readSurveyForm(self, request):
        print('사용자 전용')