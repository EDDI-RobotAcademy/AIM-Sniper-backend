from django.db import models

from survey.entity.survey_question import SurveyQuestion


class SurveySelection(models.Model):
    id = models.AutoField(primary_key=True)
    selection = models.CharField(max_length=50, unique=True)
    survey_question_id = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, db_column='survey_question_id')

    class Meta:
        db_table = 'survey_selection'
        app_label = 'survey'