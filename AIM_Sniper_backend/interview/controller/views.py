from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from interview.service.interview_service_impl import InterviewServiceImpl


class InterviewView(viewsets.ViewSet):
    interviewService = InterviewServiceImpl.getInstance()

    def insertSession(self, request):
        isSaved = self.interviewService.insertSession()
        return Response(isSaved, status=status.HTTP_200_OK)

    def insertFirstQuestion(self, request):
        isSaved = self.interviewService.insertFirstQuestion()
        print("첫 번째 질문 Insert 완료")
        return Response(isSaved, status=status.HTTP_200_OK)

    def getSession(self, request):
        sessionId = request.data.get('sessionId')
        print('데이터를 잘 불러왔나?:', sessionId)
        questionList = self.interviewService.getSession(sessionId)
        return Response({'questionList': questionList}, status=status.HTTP_200_OK)

    def getFirstQuestion(self, request):
        questionId = request.data.get('questionId')
        print('questionId:', questionId)
        firstQuestion = self.interviewService.getFirstQuestion(questionId)
        return Response({'firstQuestion': firstQuestion}, status=status.HTTP_200_OK)
