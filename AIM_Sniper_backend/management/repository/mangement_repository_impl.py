from win32comext.axscript.client.framework import profile

from account.entity.account_role_type import AccountRoleType
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from management.repository.mangement_repository import ManagementRepository
from account.entity.profile import Profile
from marketing.entity.models import Marketing


class ManagementRepositoryImpl(ManagementRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__profileRepository = ProfileRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def userList(self):
        # Profile과 Account 정보를 가져오기 위한 쿼리
        profiles = Profile.objects.select_related('account', 'gender').all()

        # 결과를 프론트엔드가 원하는 형식으로 변환
        userList = []
        for profile in profiles:
            user_data = {
                "userId": profile.account.id,  # Account의 id
                "email": profile.email,
                "gender": profile.gender.gender_type,  # ProfileGenderType에서 gender 이름 가져오기
                "birthyear": profile.birthyear,
                "login_type": profile.account.loginType.loginType,  # AccountLoginType에서 로그인 타입 이름 가져오기
                "role_type": profile.account.roleType.roleType,  # AccountRoleType에서 role 타입 이름 가져오기
                "last_login": profile.last_login,
            }
            userList.append(user_data)
        print(userList)
        return userList

    def grantRoleType(self, email):
        profile = self.__profileRepository.findByEmail(email)
        admin_role = AccountRoleType.objects.get(roleType='ADMIN')
        profile.account.roleType = admin_role
        profile.account.save()
        return profile


    def revokeRoleType(self, email):
        profile = self.__profileRepository.findByEmail(email)
        NORMAL = AccountRoleType.objects.get(roleType='NORMAL')
        profile.account.roleType = NORMAL
        profile.account.save()
        return profile

