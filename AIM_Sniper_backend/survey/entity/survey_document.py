from django.db import models


class SurveyDocument(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'survey_document'
        app_label = 'survey'