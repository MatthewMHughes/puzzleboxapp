from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db import transaction
from django.db.utils import OperationalError
import json
import time
from pusher import Pusher
from .models import Dial

import pusher

pusher_client = pusher.Pusher(
  app_id='1834159',
  key='983d24044a46cf1a6470',
  secret='5572c6e422303a1277cc',
  cluster='eu',
  ssl=True
)

def sendMoveDialMessage(request):
        # check if the method is post
        if request.method == 'POST':
            data = request.body
            # data is a bytes-like object, so you might want to convert it to a dictionary or a string
            data = data.decode('utf-8')
            # parse the JSON data
            data = json.loads(data)
            print(data)
            # try form validation
            pusher_client.trigger('puzzlebox', data['post_data']["event"], {"dialNumber": int(data['post_data']["dialNumber"]), "username": data['post_data']["username"]})
            return HttpResponse('ok')

class IndexView(generic.ListView):
    template_name = "puzzlebox/index.html"
    context_object_name = "dials"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        data = Dial.objects.filter().order_by("dialNumber")
        newData = []
        for item in data:
            item = model_to_dict(item)
            newData.append(item)
        return newData
    
def complete(request):
    return render(request,"puzzlebox/complete.html")

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65)
def prev_alpha(s):

    print(s, chr((ord(s.upper())-1 - 65) % 26 + 65))
    return chr((ord(s.upper())-1 - 65) % 26 + 65)

def movedial(request):
   #the request method is checked to make sure it is a POST request
    if request.method == "POST":
        #the request body is accessed using request.body, which contains the raw request payload
        data = request.body
        # data is a bytes-like object, so you might want to convert it to a dictionary or a string
        data = data.decode('utf-8')
        # parse the JSON data
        data = json.loads(data)
        savedData = False
        complete = True
        while savedData == False:
            try:
                with transaction.atomic():
                    dials = Dial.objects.select_for_update().filter().order_by("dialNumber")
                    newData = []
                    for item in dials:
                        item = model_to_dict(item)
                        newData.append(item)
                    movedDial = newData[data['post_data']["dialNumber"] - 1]
                    movedPiston1 = newData[movedDial["firstLink"] - 1]
                    movedDir1 = movedDial["firstLinkDir"] * data['post_data']["moveDir"]
                    movedPiston2 = newData[movedDial["secondLink"] - 1]
                    movedDir2 = movedDial["secondLinkDir"] * data['post_data']["moveDir"]
                    movePistons = False
                    if data['post_data']["moveDir"] == 1:
                        if movedDial["dialPosition"] < 25:
                            movePistons = True
                            movedDial["dialLetter"] = next_alpha(movedDial["dialLetter"])
                            movedDial["dialPosition"]+=1
                            if movedDial["pistonPosition"] == 5:
                                movedDial["pistonPosition"] = 0
                            else:
                                movedDial["pistonPosition"]+=1
                    else:
                        if movedDial["dialPosition"] > -25:
                            movePistons = True
                            movedDial["dialLetter"] = prev_alpha(movedDial["dialLetter"])
                            movedDial["dialPosition"]-=1
                            if movedDial["pistonPosition"] == 0:
                                movedDial["pistonPosition"] = 5
                            else:
                                movedDial["pistonPosition"]-=1
                    if movePistons:
                        if movedDir1 == 1:
                            if movedPiston1["pistonPosition"] == 5:
                                movedPiston1["pistonPosition"] = 0
                            else:
                                movedPiston1["pistonPosition"]+=1
                        else:
                            if movedPiston1["pistonPosition"] == 0:
                                movedPiston1["pistonPosition"] = 5
                            else:
                                movedPiston1["pistonPosition"]-=1
                        if movedDir2 == 1:
                            if movedPiston2["pistonPosition"] == 5:
                                movedPiston2["pistonPosition"] = 0
                            else:
                                movedPiston2["pistonPosition"]+=1
                        else:
                            if movedPiston2["pistonPosition"] == 0:
                                movedPiston2["pistonPosition"] = 5
                            else:
                                movedPiston2["pistonPosition"]-=1
                    Dial.objects.filter(dialNumber=data['post_data']["dialNumber"]).update(pistonPosition=movedDial["pistonPosition"], dialPosition=movedDial["dialPosition"], dialLetter=movedDial["dialLetter"])   
                    Dial.objects.filter(dialNumber=movedPiston1["dialNumber"]).update(pistonPosition=movedPiston1["pistonPosition"], dialPosition=movedPiston1["dialPosition"])   
                    Dial.objects.filter(dialNumber=movedPiston2["dialNumber"]).update(pistonPosition=movedPiston2["pistonPosition"], dialPosition=movedPiston2["dialPosition"])    
                    savedData = True
                    updatedDials = Dial.objects.filter().order_by("dialNumber")
                    updatedData = []
                    for item in updatedDials:
                        item = model_to_dict(item)
                        updatedData.append(item)
                    for dial in updatedData:
                        print(dial["pistonPosition"])
                        if dial["pistonPosition"] != 3:
                            print("lol")
                            complete = False
            except OperationalError:
                time.sleep(1)
        # return a JSON response
        if(complete):
            pusher_client.trigger('puzzlebox', "complete", {})
        return JsonResponse({'message': 'Data received'},safe=False)
    else:
        return JsonResponse({'error': 'Bad request'}, status=400)