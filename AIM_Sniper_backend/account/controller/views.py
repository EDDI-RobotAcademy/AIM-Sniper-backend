import hashlib
import os
import uuid
import random
import string

from dotenv import load_dotenv
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.repository.account_repository_impl import AccountRepositoryImpl
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.serializers import AccountSerializer
from account.service.account_service_impl import AccountServiceImpl
from redis_service.service.redis_service_impl import RedisServiceImpl


class AccountView(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()
    accountRepository = AccountRepositoryImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()

    load_dotenv()

    def checkEmailDuplication(self, request):
        print("checkEmailDuplication()")

        try:
            print(f"request.data: {request.data}")
            email = request.data.get("email")
            print(f"email: {email}")
            isDuplicate = self.accountService.checkEmailDuplication(email)
            print(f"isDuplicate: {isDuplicate}")

            return Response(
                {
                    "isDuplicate": isDuplicate,
                    "message": (
                        "Email이 이미 존재" if isDuplicate else "Email 사용 가능"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("이메일 중복 체크 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("비밀번호 확인 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
