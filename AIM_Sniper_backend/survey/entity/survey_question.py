from django.db import models

from survey.entity.survey import Survey


class SurveyQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=128, unique=True)
    question_type = models.CharField(max_length=10)
    essential = models.BooleanField()
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)

    class Meta:
        db_table = 'survey_question'
        app_label = 'survey'