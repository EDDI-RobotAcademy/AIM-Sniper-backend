from rest_framework import viewsets, status
from rest_framework.response import Response

from interview_result.service.interview_result_service_impl import InterviewResultServiceImpl

class InterviewResultView(viewsets.ViewSet):
    interviewResultService = InterviewResultServiceImpl.getInstance()

    def saveInterviewResult(self, request):
        try:
            scoreResultList = request.data.get('scoreResultList') # 질문, 답변, 의도, 점수+피드백

            accountId = request.data.get('accountId')

            self.interviewResultService.saveInterviewResult(scoreResultList, accountId)

            return Response(True, status=status.HTTP_200_OK)

        except Exception as e :
            print('interview result 저장중 error: ', e)

    def getInterviewResult(self, request):
        accountId = request.data.get('accountId')
        interviewResultList = self.interviewResultService.getInterviewResult(accountId)
        return Response({'interviewResultList': interviewResultList}, status=status.HTTP_200_OK)