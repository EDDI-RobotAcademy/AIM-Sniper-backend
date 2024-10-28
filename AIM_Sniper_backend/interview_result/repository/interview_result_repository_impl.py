from abc import ABC, abstractmethod

from interview_result.entity.interview_result import InterviewResult
from interview_result.entity.interview_result_qas import InterviewResultQAS
from interview_result.repository.interview_result_repository import InterviewResultRepository


class InterviewResultRepositoryImpl(InterviewResultRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def registerInterviewResult(self, account):
        InterviewResult.objects.create(account=account)
        interviewResult = InterviewResult.objects.all()
        return interviewResult.last()


    def registerInterviewResultQAS(self, interviewResult, scoreResultList):
        for scoreResult in scoreResultList:
            print(scoreResult)
            question, answer, intent, feedback = scoreResult

            InterviewResultQAS.objects.create(question=question, answer=answer, intent=intent,
                                              feedback=feedback, interview_result=interviewResult)

    def getLastInterviewResult(self):
        interviewResult = InterviewResult.objects.all()
        return interviewResult.last()

    def getLastInterviewResultQASList(self, interviewResult):
        interviewResult = InterviewResultQAS.objects.filter(interview_result=interviewResult)
        interviewResultQASList = interviewResult.order_by('id').values_list('question', 'answer', 'intent', 'feedback')
        return interviewResultQASList

