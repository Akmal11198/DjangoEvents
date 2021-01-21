from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EventSerializer, UserSerializer, participationSerializer
from datetime import date
from operator import attrgetter
from .models import Event, User, Participation
import json
# Create your views here.


# get all users
@api_view(['GET'])
def users(request):
    allUsers = User.objects.all()
    serial = UserSerializer(allUsers, many=True)
    return Response(serial.data)


# login
@api_view(['POST'])
def login(request):
    try:
        body = json.loads(request.body)
        user = body.get('email', None)
        password = body.get('password', None)

        if not user:
            return Response(data={'msg': "no email was entered"}, status=400)

        try:
            user = User.objects.get(email=user)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response(data={'msg': "no such user was found in the database"}, status=400)

        if not password:
            return Response(data={'msg': "no password was entered"}, status=400)
        if user.password != password:
            return Response(data={'msg': "Password is incorrect"}, status=400)
        serialU = UserSerializer(user, many=False)
        return Response(serialU.data)
    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# register
@api_view(['POST'])
def register(request):
    try:
        body = json.loads(request.body)
        email = body.get('email', None)
        password = body.get('password', None)

        if not email:
            return Response(data={'msg': "no email was entered"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            return Response(data={'msg': "This email is already registered"}, status=400)

        if not password:
            return Response(data={'msg': "no password was entered"}, status=400)
        newUser = User.objects.create(email=email, password=password)
        newUser.save()
        serialU = UserSerializer(newUser, many=False)
        return Response(serialU.data)
    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# get all events
@api_view(['GET'])
def allEvents(request):
    allEvents = Event.objects.all().order_by('date')
    serial = EventSerializer(allEvents, many=True)
    return Response(serial.data)


# get events that the user signed up for
@api_view(['GET'])
def joinedEvents(request, email=None):
    try:
        if not email:
            return Response(data={'msg': "no user is logged in"}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if not user:
            return Response(data={'msg': "no such user was found in the database"}, status=400)
        try:
            ps = Participation.objects.filter(participant=user)
        except Participation.DoesNotExist:
            ps = None
        if not ps:
            return Response(data={'msg': "you have not joined any events yet"}, status=400)
        joinedEvents = []
        for p in ps:
            try:
                event = Event.objects.get(title=p.event.title)
                joinedEvents.append(event)
            except Event.DoesNotExist:
                event = None
        joinedEvents.sort(key=attrgetter('date'))
        serial = EventSerializer(joinedEvents, many=True)
        return Response(serial.data)
    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# get events created by this user
@api_view(['GET'])
def createdEvents(request, email=None):
    try:
        if not email:
            return Response(data={'msg': "no user is logged in"}, status=400)
        try:
            creator = User.objects.get(email=email)
        except User.DoesNotExist:
            creator = None
        if not creator:
            return Response(data={'msg': "no such user was found in the database"}, status=400)
        creatorSerializer = UserSerializer(creator, many=False)
        createdEvents = Event.objects.filter(creator=creator).order_by('date')
        if len(createdEvents) == 0:
            return Response(data={'msg': "you have not created any events yet"}, status=400)
        serial = EventSerializer(createdEvents, many=True)
        return Response(serial.data)
    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# add event
@api_view(['POST'])
def addEvent(request):
    try:
        body = json.loads(request.body)
        creator = body.get('creator', None)
        title = body.get('title', None)
        description = body.get('description', "")
        eventDate = body.get('date', date.today())

        if not creator:
            return Response(data={'msg': "no user is logged in"}, status=400)

        try:
            creator = User.objects.get(email=creator)
        except User.DoesNotExist:
            creator = None

        if not creator:
            return Response(data={'msg': "no such user was found in the database"}, status=400)

        if not title:
            return Response(data={'msg': "You have not set an event title"}, status=400)

        try:
            sameEvent = Event.objects.get(title=title)
        except Event.DoesNotExist:
            sameEvent = None

        if sameEvent:
            return Response(data={'msg': "An event with the same title already exists"}, status=400)

        newEvent = Event.objects.create(
            creator=creator, title=title, description=description, date=eventDate)
        newEvent.save()
        newParticipation = Participation.objects.create(
            event=Event.objects.get(title=title), participant=creator)
        newParticipation.save()
        serializedEvent = EventSerializer(newEvent, many=False)
        return Response(serializedEvent.data)

    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# update event
@api_view(['PUT'])
def editEvent(request):
    try:
        body = json.loads(request.body)
        creator = body.get('creator', None)
        title = body.get('title', None)
        description = body.get('description', None)
        eventDate = body.get('date', None)

        if not creator:
            return Response(data={'msg': "no user is logged in"}, status=400)

        try:
            creator = User.objects.get(email=creator)
        except User.DoesNotExist:
            creator = None

        if not creator:
            return Response(data={'msg': "no such user was found in the database"}, status=400)

        if not title:
            return Response(data={'msg': "You have not set an event title"}, status=400)

        try:
            curEvent = Event.objects.get(title=title)
        except Event.DoesNotExist:
            curEvent = None

        if not curEvent:
            return Response(data={'msg': "No event with the same title was found"}, status=400)

        if curEvent.creator.email != creator.email:
            return Response(data={'msg': "You are unauthorized to edit this event"}, status=401)

        if description:
            curEvent.description = description
        if eventDate:
            curEvent.date = eventDate
        curEvent.save()
        serializedEvent = EventSerializer(curEvent, many=False)
        return Response(serializedEvent.data)

    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# sign up for an event
@api_view(['POST'])
def joinEvent(request):
    try:
        body = json.loads(request.body)
        user = body.get('email', None)
        title = body.get('title', None)

        if not user:
            return Response(data={'msg': "no user is logged in"}, status=400)

        try:
            user = User.objects.get(email=user)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response(data={'msg': "no such user was found in the database"}, status=400)

        if not title:
            return Response(data={'msg': "You have not set an event title"}, status=400)

        try:
            event = Event.objects.get(title=title)
        except Event.DoesNotExist:
            event = None

        if not event:
            return Response(data={'msg': "No event of this title was found"}, status=400)

        try:
            newParticipation = Participation.objects.get(
                event=event, participant=user)
        except Participation.DoesNotExist:
            newParticipation = None

        if newParticipation:
            return Response(data={'msg': "You are already signed-up for this event "}, status=400)

        newParticipation = Participation.objects.create(
            event=event, participant=user)
        newParticipation.save()
        serialP = participationSerializer(newParticipation, many=False)
        return Response(serialP.data)

    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)


# withdraw from an event
@api_view(['DELETE'])
def exitEvent(request):
    try:
        body = json.loads(request.body)
        user = body.get('email', None)
        title = body.get('title', None)

        if not user:
            return Response(data={'msg': "no user is logged in"}, status=400)

        try:
            user = User.objects.get(email=user)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response(data={'msg': "no such user was found in the database"}, status=400)

        if not title:
            return Response(data={'msg': "You have not set an event title"}, status=400)

        try:
            event = Event.objects.get(title=title)
        except Event.DoesNotExist:
            event = None

        if not event:
            return Response(data={'msg': "No event of this title was found"}, status=400)

        try:
            delParticipation = Participation.objects.get(
                event=event, participant=user)
        except Participation.DoesNotExist:
            delParticipation = None

        if not delParticipation:
            return Response(data={'msg': "You are not signed-up for this event"}, status=400)

        Participation.objects.get(event=event, participant=user).delete()
        serialP = participationSerializer(delParticipation, many=False)
        return Response(serialP.data)

    except Exception as e:
        return Response(data={'msg': str(e)}, status=500)
