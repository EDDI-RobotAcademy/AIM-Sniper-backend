from django.db import models

from survey.entity.survey_document import SurveyDocument


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    survey_document_id = models.ForeignKey(SurveyDocument, on_delete=models.CASCADE)


    class Meta:
        db_table = 'survey'
        app_label = 'survey'