from rest_framework import serializers
from .models import User,Participation,Event

class UserSerializer(serializers.ModelSerializer):
    createdEvents=serializers.SerializerMethodField('get_createdEvents')
    joinedEvents=serializers.SerializerMethodField('get_joinedEvents')

    class Meta:
        model = User
        fields = ['email','password','createdEvents','joinedEvents']

    def get_createdEvents(self,user):
        created=Event.objects.filter(creator=user.email)
        return map(lambda event:event.title,created)

    def get_joinedEvents(self,user):
        participation=Participation.objects.filter(participant=user.email)
        return map(lambda p:p.event.title,participation)


class EventSerializer(serializers.ModelSerializer):
    participants=serializers.SerializerMethodField('get_participants')
    class Meta:
        model = Event
        fields = ['title','description','date','creator','participants']
    
    def get_participants(self,event):
        all=Participation.objects.filter(event=event.title)
        return map(lambda p:p.participant.email, all)



class participationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'