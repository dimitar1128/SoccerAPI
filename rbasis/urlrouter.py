from rest_framework import routers

class ApiRouter:
    router = routers.DefaultRouter()
    def register(self, regex, classobject, name, base_name=None):
        self.router.register(regex, classobject, name, base_name)
    def urls(self):
        return self.router.urls

router = ApiRouter()

