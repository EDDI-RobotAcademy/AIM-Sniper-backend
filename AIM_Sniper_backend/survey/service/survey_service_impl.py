from survey.repository.survey_description_repository_impl import SurveyDescriptionRepositoryImpl
from survey.repository.survey_repository_impl import SurveyRepositoryImpl
from survey.repository.survey_title_repository_impl import SurveyTitleRepositoryImpl
from survey.service.survey_service import SurveyService


class SurveyServiceImpl(SurveyService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            # cls.__instance.__surveyDocumentRepository = SurveyDocumentRepositoryImpl.getInstance()
            cls.__instance.__surveyRepository = SurveyRepositoryImpl.getInstance()
            cls.__instance.__surveyTitleRepository = SurveyTitleRepositoryImpl.getInstance()
            cls.__instance.__surveyDescriptionRepository = SurveyDescriptionRepositoryImpl.getInstance()
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

    def getSurveyBySurveyId(self, surveyId):
        survey = self.__surveyRepository.findSurvey(surveyId)
        return survey

    def registerTitleDescription(self, survey, surveyTitle, surveyDescription):
        try:
            titleResult = self.__surveyTitleRepository.registerTitle(survey, surveyTitle)
            descriptionResult = self.__surveyDescriptionRepository.registerDescription(survey, surveyDescription)
            return titleResult & descriptionResult
        except Exception as e:
            print('설문 제목, 설명 저장 중 오류 발생 : ', e)
            return False

    def registerQuestion(self, question):
        pass

    def registerSelection(self, selection):
        pass


    def readSurveyForm(self):
        print('사용자 전용')



