from rest_framework import viewsets, status
from rest_framework.response import Response

from survey.entity.survey import Survey
from survey.entity.survey_answer import SurveyAnswer
from survey.entity.survey_description import SurveyDescription
from survey.entity.survey_document import SurveyDocument
from survey.entity.survey_question import SurveyQuestion
from survey.entity.survey_selection import SurveySelection
from survey.entity.survey_title import SurveyTitle


class SurveyView(viewsets.ViewSet):

    def create(self, request):
        print('controller -> createSurvey')
        print(Survey,
        SurveyDocument,
        SurveyQuestion,
        SurveyAnswer,
        SurveyTitle,
        SurveySelection,
        SurveyDescription)