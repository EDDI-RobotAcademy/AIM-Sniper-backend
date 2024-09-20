from abc import ABC, abstractmethod

class GoogleOauthService(ABC):
    @abstractmethod
    def googleLoginAddress(self):
        pass

