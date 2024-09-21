from django.db import models

from survey.entity.survey_question import SurveyQuestion
from survey.entity.survey_selection import SurveySelection

class SurveyAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    survey_selection_id = models.ForeignKey(SurveySelection, on_delete=models.CASCADE, db_column='survey_selection_id')
    survey_question_id = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, db_column='survey_question_id')

    class Meta:
        db_table = 'survey_answer'
        app_label = 'survey'