from rest_framework import viewsets, status
from rest_framework.response import Response
from survey.service.survey_service_impl import SurveyServiceImpl

class SurveyView(viewsets.ViewSet):
    surveyService = SurveyServiceImpl.getInstance()

    def createSurveyForm(self, request):
        surveyId = self.surveyService.createSurveyForm()
        return Response(surveyId, status=status.HTTP_200_OK)

    def registerTitleDescription(self, request):
        print('registerTitleDescription')


    def registerQuestion(self, request):
        pass

    def registerSelection(self, request):
        pass
    def readSurveyForm(self, request):
        print('사용자 전용')