from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountType(models.Model):
    accounttypeid = models.AutoField(primary_key = True)
    accounttypename = models.CharField(max_length=250, blank=True, null=True)
    shortname = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'AccountType'

# User gồm: ID, username, password, first_name, last_name, email.

class Account(models.Model):
    accountid = models.AutoField(primary_key = True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userid')
    accounttypeid = models.ForeignKey(AccountType, models.DO_NOTHING, blank=True, null=True)
    phonenumber = models.CharField(max_length=250, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    job = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Account'


# NEO4J
from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo

# Create your models here.
# 02
class Exam(StructuredNode):
    examid = UniqueIdProperty()
    owner = StringProperty(required=True)
    examname = StringProperty(required=True)
    description = StringProperty(required=True)

class ExamBatch(StructuredNode):
    exambatchid = UniqueIdProperty()
    pincode = StringProperty(required=True)
    timebatch = StringProperty(required=True)
    # Relations:
    examrel = RelationshipTo(Exam, 'batch_belongto_exam')

class Question(StructuredNode):
    questionid = UniqueIdProperty()
    content = StringProperty(required=True)
    A = StringProperty(required=True)
    B = StringProperty(required=True)
    C = StringProperty(required=True)
    D = StringProperty(required=True)
    answer = StringProperty(required=True)
    # Relations:
    examrel = RelationshipTo(Exam, 'question_belongto_exam')

# 03
class Contestant(StructuredNode):
    contestantid = UniqueIdProperty()
    contestantname = StringProperty(required=True)
    # Relations:
    exambatchrel = RelationshipTo(ExamBatch, 'contestant_belongto_batch')

class Result(StructuredNode):
    resultid = UniqueIdProperty()
    choice = StringProperty(required=True)
    iscorrect = IntegerProperty(required=True)
    # Relations:
    contestantrel = RelationshipTo(Contestant, 'result_belongto_contestant')
    questionrel = RelationshipTo(Question, 'result_belongto_question')