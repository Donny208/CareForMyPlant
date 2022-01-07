from mongoengine import *


connect('plant', host='127.0.0.1', port=27017)


class User(Document):
    username = StringField(required=True)
    votes = ListField(IntField(), default=[0, 0])
    points = IntField(default=0)
    streak = IntField(default=0)
    meta = {'collection': 'users'}


class Vote(Document):
    date = StringField(required=True)
    post_id = StringField(required=True)
    outcome = IntField(default=-1)
    voters = ListField(ReferenceField('User'), default=[])
    details = DictField(default={})
    meta = {'collection': 'votes'}


class Data(Document):
    timestamp = StringField(required=True)
    temperature = FloatField(required=True)
    moisture = FloatField(required=True)
    light = IntField(required=True)
    conductivity = IntField(required=True)
    battery = IntField(required=True)
    meta = {'collection': 'data'}
