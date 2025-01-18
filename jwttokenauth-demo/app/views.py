from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class HelloView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request):
        content = {'message':'Hello This is Message from api'}
        return Response(content)

def index(request):
    return render(request,'index.html')