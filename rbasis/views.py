from rest_framework import viewsets

class ShAPIView(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        res = super().list(request,args,kwargs)
        return res

    def update(self, request, *args, **kwargs):
        res = super().update(request,args,**kwargs)
        return res

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request,args,kwargs)
        return res

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request,args,kwargs)
        return res

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request,args,kwargs)
        return res

    def create(self, request, *args, **kwargs):
        res = super().create(request,args,kwargs)
        return res