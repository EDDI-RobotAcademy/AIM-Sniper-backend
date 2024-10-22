import glob
import json
import os

from interview.repository.interview_repository_impl import InterviewRepositoryImpl
from interview.service.interview_service import InterviewService


class InterviewServiceImpl(InterviewService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__interviewRepositoryImpl = InterviewRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def insertSession(self):
        questionFiles = glob.glob(os.path.join('assets/json_qa_pair', '*.json'))
        for questionFile in questionFiles:
            questionList = []
            with open(questionFile, 'r', encoding='utf-8') as file:
                print('열려는 qu file: ', questionFile)
                data = json.load(file)
                for dic in data:
                    questionList.append(dic.get('question'))
            interviewId = self.__interviewRepositoryImpl.getMaxId()
            self.__interviewRepositoryImpl.insertData(interviewId+1, questionList)
        print('저장 완료')

        return True

    def getSession(self, sessionId):
        questionList = self.__interviewRepositoryImpl.getData(sessionId)
        return questionList