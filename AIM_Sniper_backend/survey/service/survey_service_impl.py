from survey.repository.survey_repository_impl import SurveyRepositoryImpl
from survey.service.survey_service import SurveyService


class SurveyServiceImpl(SurveyService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            # cls.__instance.__surveyDocumentRepository = SurveyDocumentRepositoryImpl.getInstance()
            cls.__instance.__surveyRepository = SurveyRepositoryImpl.getInstance()
            # cls.__instance.__surveyTitleRepository = SurveyTitleRepositoryImpl.getInstance()
            # cls.__instance.__surveyDescriptionRepository = SurveyDescriptionRepositoryImpl.getInstance()
            # cls.__instance.__surveyQuestionRepository = SurveyQuestionRepositoryImpl.getInstance()
            # cls.__instance.__surveySelectionRepository = SurveySelectionRepositoryImpl.getInstance()
            # cls.__instance.__surveyAnswerRepository = SurveyAnswerRepositoryImpl.getInstance()


        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createSurveyForm(self):
        maxId = self.__surveyRepository.getMaxId()
        surveyId = self.__surveyRepository.registerSurvey(maxId+1)
        return surveyId

    def registerTitleDescription(self, title, description):
        pass

    def registerQuestion(self, question):
        pass

    def registerSelection(self, selection):
        pass


    def readSurveyForm(self):
        print('사용자 전용')




