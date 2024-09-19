from account.entity.account import Account
from account.entity.account_login_type import AccountLoginType
from account.entity.account_role_type import AccountRoleType
from account.repository.account_repository import AccountRepository

from django.utils import timezone

class AccountRepositoryImpl(AccountRepository):
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

    def create(self, loginType, roleType):
        loginTypeEntity = AccountLoginType.objects.get_or_create(loginType=loginType)
        roleTypeEntity = AccountRoleType.objects.get_or_create(roleType=roleType)
        loginType = loginTypeEntity[0]
        roleType = roleTypeEntity[0]

        account = Account.objects.create(loginType=loginType, roleType=roleType)
        return account

