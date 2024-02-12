
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
q = []


@api_view(['POST'])
def push(request):
    print(request.data)
    q.append((request.data['key'], request.data['value']))
    print(q)
    return Response("received", status=status.HTTP_200_OK,content_type="application/json")


@api_view(['GET'])
def pull(request):
    print(request.data)
    if(len(q)==0):
        return Response("saf khalie",status=status.HTTP_400_BAD_REQUEST)
    else:
        b=q.pop(0)
        print(b)
        data = {
            'key' : b[0],
            'value' : b[1]
        }
        return Response(data)

