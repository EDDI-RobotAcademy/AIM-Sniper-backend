from django.db import models

from survey.entity.survey import Survey


class SurveyTitle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)

    class Meta:
        db_table = 'survey_title'
        app_label = 'survey'