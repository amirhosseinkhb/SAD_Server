import threading
from queue import Queue

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import asyncio
import websockets

# Create your views here.
q = []
subscribers = Queue()


def notify_subscriber():
    if subscribers.not_empty:
        subscriber = subscribers.get()
        try:
            if len(q) != 0:
                pull(subscriber)
            else:
                print("no message to notify")
        except Exception as e:
            print(f"Error in pull function: {e}")
        subscribers.put(subscriber)
    else:
        print("No subscribers to notify.")


def notify_subscribe():
    if len(q) != 0:
        subscriber = subscribers.get()
        data = getMessage()
        subscribers.put(subscriber)
        return data
    else:return 0

def getMessage():
    if len(q) == 0:
        data = {
            'key': '1',
            'value': 'no message found!'
        }
    else:
        b = q.pop(0)
        print(b)
        data = {
            'key': b[0],
            'value': b[1]
        }
    return data


@api_view(['POST'])
def push(request):
    q.append((request.data['key'], request.data['value']))
    print(q)
    thread = threading.Thread(target=notify_subscriber)
    thread.start()
    return Response("received", status=status.HTTP_200_OK, content_type="application/json")


@api_view(['GET'])
def subscribe(request):
    subscribers.put(request._request)
    data = notify_subscribe()
    while(data==0):
        data=notify_subscriber()
    return Response(data, status=status.HTTP_200_OK)




@api_view(['GET'])
def pull(request):
    data = getMessage()
    return Response(data)
