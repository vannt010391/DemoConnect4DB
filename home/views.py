from functools import partial
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from neomodel.properties import JSONProperty
from home.models import *
# Create your views here.
import random
import  pymongo 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["result"]

def test(request):
    mydict = { "name": "John", "address": "Highway 37" }
    
    print(x.inserted_id)
    print(myclient.list_database_names())
    dblist = myclient.list_database_names()
    if "mydatabase" in dblist:
        print("The database exists.")

    for x in mycol.find():
        print(x)
    
    context = {
    
           
        }
    return render(request, 'home/test.html', context)


def index(request):
    if request.user.is_authenticated: 
        is_log = 1
        user=request.user
        context = {
            'user':user,
            'is_log':is_log
        }
        return render(request, 'home/index.html', context)
    else:
        is_log = 0
        context = {
            'is_log':is_log
        }
        return render(request, 'home/index.html', context)

def MyLogin(request):
    if request.user.is_authenticated: 
        return redirect('home:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')  
            user = authenticate(username=username, password=password)
            if user is not None: 
                if user.is_active: 
                    login(request, user)
                    return redirect('home:index')
                else:
                    return render(request, 'home/login.html', {'message':'Tài khoản đã bị vô hiệu hóa'})
            else:
                return render(request, 'home/login.html', {'message':'Tài khoản không tồn tại'})

        return render(request, 'home/login.html')


def MyLogout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('home:login')

def MyRegister(request):
    if request.user.is_authenticated:
        return redirect('home:index')
    else:
        if request.method == 'POST':    
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if username == '' or password1 == '' or password2 == '' or password1 != password2:
                return render(request, 'home/register.html',{'message':'password hoặc username không hợp lệ'})
            else:
                new_user = User()
                new_user.username = username
                new_user.set_password(password1)
                new_user.save()
                user = authenticate(username=username, password=password1)
                login(request, user)

                new_account = Account()
                new_account.userid = new_user
                new_account.accounttypeid = AccountType.objects.get(accounttypeid=1)
        
                new_account.save()

                return redirect('home:index')

        return render(request, 'home/register.html')

def MyExam(request):
    if request.user.is_authenticated: 
        user=request.user
        getuserid = user.id 
        allexam = Exam.nodes.filter(owner = getuserid)

        if request.method == 'POST':    
            examname = request.POST.get('examname')
            description = request.POST.get('description')
            
            exam = Exam(owner=getuserid, examname=examname, description=description)
            exam.save()

            return redirect('home:exam')

        context = {
            'user':user,
            'allexam': allexam
        }
        return render(request, 'home/myexam.html', context)
    else:
        return redirect('home:login')

def EditExam(request, id):
    if request.user.is_authenticated: 
        user=request.user
        
        getexam = Exam.nodes.get(examid = id)

    
        if request.method == 'POST':    
            examname = request.POST.get('examname')
            description = request.POST.get('description')

            getexam.examname = examname
            getexam.description = description
            getexam.save()

            return redirect('home:exam')
        else:
            context = {

                'user':user,
                'exam': getexam
            }
            return render(request, 'home/editexam.html', context)
    else:
        return redirect('home:login')


def DelExam(request, id):
    if request.user.is_authenticated: 
        getexam = Exam.nodes.get(examid = id)
        getexam.delete()

        return redirect('home:exam')
    else:
        return redirect('home:login')


from neomodel import Traversal, INCOMING
class QuestionMod:
    def __init__(self, order, question):
        self.order = order
        self.question = question



def questionexam(request,id):
    if request.user.is_authenticated: 
        user=request.user
        getuserid = user.id 

        exam = Exam.nodes.get(examid = id)

        definition = dict(node_class=Question, direction=INCOMING, relation_type=None, model=None)
        getTraversals = Traversal(exam, Question.__label__, definition)

        allquestion = []
        order = 0
        
        for getTraversal in getTraversals:
            order += 1
            new_ques_mod = QuestionMod(order, getTraversal)
            allquestion.append(new_ques_mod)

    
        if request.method == 'POST':    
            content = request.POST.get('content')
            chA = request.POST.get('chA')
            chB = request.POST.get('chB')
            chC = request.POST.get('chC')
            chD = request.POST.get('chD')
            chAns = request.POST.get('chAns')

            
            question = Question(content=content, A=chA, B=chB, C=chC, D=chD, answer=chAns)
            question.save()
            question.examrel.connect(exam)
            
            return redirect('home:questionexam', exam.examid)

        context = {
            'user':user,
            'exam': exam,
            'allquestion': allquestion
        }
        return render(request, 'home/questionexam.html', context)
    else:
        return redirect('home:login')

def EditQuestion(request, id):
    if request.user.is_authenticated: 
        user=request.user
        
        getquestion = Question.nodes.get(questionid = id)
        examid = getquestion.examrel[0].examid
        thischAns = int(getquestion.answer)
    
        if request.method == 'POST':    
            content = request.POST.get('content')
            chA = request.POST.get('chA')
            chB = request.POST.get('chB')
            chC = request.POST.get('chC')
            chD = request.POST.get('chD')
            chAns = request.POST.get('chAns')

            getquestion.content = content
            getquestion.A = chA
            getquestion.B = chB
            getquestion.C = chC
            getquestion.D = chD
            getquestion.answer = chAns

            getquestion.save()

            return redirect('home:questionexam', examid)
        else:
            context = {
                'user': user,
                'examid':examid,
                'question': getquestion,
                'thischAns':thischAns
            }
            return render(request, 'home/editquestion.html', context)
    else:
        return redirect('home:login')

def DelQuestion(request, id):
    if request.user.is_authenticated: 
        getquestion = Question.nodes.get(questionid = id)
        examid = getquestion.examrel[0].examid
        
        getquestion.delete()

        return redirect('home:questionexam', examid)
    else:
        return redirect('home:login')


def inputpin(request):
    
    if request.method == 'POST':
        inputpin = request.POST.get('inputpin')
        yourname = request.POST.get('yourname')
        try:
            exambatch = ExamBatch.nodes.get(pincode = inputpin)

            examid = exambatch.examrel[0].examid
            exam = Exam.nodes.get(examid = examid)

            contestant = Contestant(contestantname=yourname, timebatch=5)
            contestant.save()
            contestant.exambatchrel.connect(exambatch)
            request.session['contestant'] = str(contestant.contestantid)

            definition = dict(node_class=Question, direction=INCOMING, relation_type=None, model=None)
            all_question = Traversal(exam, Question.__label__, definition)

            
            
            doc_contest =  {
                '_id': contestant.contestantid,
                'exambatchid': exambatch.exambatchid,
                'result' : 0,
            }
            order = 1
            for question in all_question:
               
                doc_contest[str(order)] = 0
                order += 1
                
            
            x = mycol.insert_one(doc_contest)


            return redirect('home:studentpin', examid)

            
        except:
            return render(request, 'home/inputpin.html', {'message':'Mã pin không chính xác'})
            

        
        

    return render(request, 'home/inputpin.html')


def teacherpin(request,id):
    if request.user.is_authenticated: 
        user=request.user
        getuserid = user.id 

        exam = Exam.nodes.get(examid = id)
        

        definition = dict(node_class=Question, direction=INCOMING, relation_type=None, model=None)
        getTraversals = Traversal(exam, Question.__label__, definition)

        allquestion = []
        order = 0

        
        a = str(random.randint(111111, 999999))
        exambatch = ExamBatch(pincode=a, timebatch=5)
        exambatch.save()
        exambatch.examrel.connect(exam)

        cache.set(exambatch.exambatchid, 0, timeout=3600)
        
        for getTraversal in getTraversals:
            order += 1
            new_ques_mod = QuestionMod(order, getTraversal)
            allquestion.append(new_ques_mod)
        
        numbques = len(allquestion)

        context = {
            'user':user,
            'exam': exam,
            'allquestion': allquestion,
            'exambatch':exambatch,
            'numbques':numbques
        }
        return render(request, 'home/teacherPin.html', context)
    else:
        return redirect('home:login')

def studentpin(request,id):
    if request.session.has_key('contestant'): 
        

        exam = Exam.nodes.get(examid = id)
        idcontestant = request.session['contestant']
        contestant = Contestant.nodes.get(contestantid = idcontestant)
        exambatch = contestant.exambatchrel[0]
        # print(exambatch.pincode)

        definition = dict(node_class=Question, direction=INCOMING, relation_type=None, model=None)
        getTraversals = Traversal(exam, Question.__label__, definition)

        allquestion = []
        order = 0

        for getTraversal in getTraversals:
            order += 1
            new_ques_mod = QuestionMod(order, getTraversal)
            allquestion.append(new_ques_mod)

        numbques = len(allquestion)
        context = {
            
            'exam': exam,
            'allquestion': allquestion,
            'numbques':numbques,
            'exambatch':exambatch
        }
        return render(request, 'home/studentpin.html', context)
    else:
        return redirect('home:login')


def result(request, id):
    if request.user.is_authenticated or request.session.has_key('contestant'): 
       

        exambatch = ExamBatch.nodes.get(exambatchid = id)
        



        context = {
            'exambatch':exambatch
        }
        return render(request, 'home/result.html', context)
    else:
        return redirect('home:login')



from django.http import JsonResponse
from django.core.cache import cache


# Ajax Area -----------------------------------------------------------------------------------
def contestantlistdiv(request):
    exambatchid = request.GET.get('exambatch', None)

    exambatch = ExamBatch.nodes.get(exambatchid=exambatchid)

    
    # print(cache.get(exambatch.exambatchid))
    # print(cache.ttl(exambatch.exambatchid))
    stage = cache.get(exambatch.exambatchid)
    definition = dict(node_class=Contestant, direction=INCOMING, relation_type=None, model=None)
    getTraversals = Traversal(exambatch, Contestant.__label__, definition)
    s = ''
    for contestant in getTraversals:

    
        temp = '''<div class="col-3 col-lg-3" style="text-align: center;margin-bottom: 10px; color: #431b93;font-weight: 900">

                    ''' + contestant.contestantname  +'''</div>'''

        s += temp
            
    data = {
                'flag':True,
                's':s,
                'stage':stage

            }
    return JsonResponse(data)




    

def startbatch(request):
    exambatchid = request.GET.get('exambatch', None)
    cache.set(exambatchid, 1 ,timeout = 3600)
    data = {
                'flag':True,
   
            }
    return JsonResponse(data)

def updateStage(request):
    exambatchid = request.GET.get('exambatch', None)
    
    stage = request.GET.get('stage', None)
    stage = int(stage)
    cache.set(exambatchid, stage ,timeout = 3600)
    data = {
                'flag':True,
   
            }
    return JsonResponse(data)


def checkStage(request):
    exambatchid = request.GET.get('exambatch', None)
    # print(exambatchid)
    stage = cache.get(exambatchid)
    
    data = {
                'flag':True,
                'stage':stage
            }
    return JsonResponse(data)



def makeChoice(request):
    choice = request.GET.get('choice', None)
    questionid = request.GET.get('questionid', None)
    order = request.GET.get('order', None)
    time = request.GET.get('time', None)

    choice = int(choice)
    order = int(order)

    idcontestant = request.session['contestant']
    contestant = Contestant.nodes.get(contestantid = idcontestant)

    question = Question.nodes.get(questionid=questionid)


    checkcorrect = 0
    if int(question.answer) == choice:
        checkcorrect = 1

    print(checkcorrect)

    new_result = Result(choice=choice, iscorrect=checkcorrect)
    new_result.save()
    new_result.contestantrel.connect(contestant)
    new_result.questionrel.connect(question)

    mydocre = mycol.find_one({"_id": contestant.contestantid}) # No result
    mydocre[str(order)] = checkcorrect
    if checkcorrect == 1:
        mydocre['result'] =  int(mydocre['result']) + 100 + (int(time)*10)
    mycol.update({'_id':contestant.contestantid},{"$set": mydocre}, upsert=False)
    mydocre = mycol.find_one({"_id": contestant.contestantid}) 

    print(mydocre)
    data = {
                'flag':True
            }
    return JsonResponse(data)

def statistic(request):
    exambatchid = request.GET.get('exambatch', None)
    stage = request.GET.get('stage', None)
    # print(exambatchid)
    exambatch = ExamBatch.nodes.get(exambatchid=exambatchid)

    definition = dict(node_class=Contestant, direction=INCOMING, relation_type=None, model=None)
    getTraversals = Traversal(exambatch, Contestant.__label__, definition)

    mydocre = mycol.find({'exambatchid':exambatchid})
    print('-----------------------------------*******')
    
    countR = mycol.find({'exambatchid':exambatchid,str(stage): 1})
    countW = mycol.find({'exambatchid':exambatchid,str(stage): 0})
    # print(countR.count())
    # print(countW.count())
    # print(stage)
        

    dataPoint = [{ 'x': 1, 'y': countR.count(), 'label': "Correct", 'color':"#E21B3C"},{ 'x': 2, 'y': countW.count(), 'label': "Incorrect", 'color':"#00ABE9"}]
    sortres_list = mycol.find({'exambatchid':exambatchid}).sort("result",-1).limit(3)
    
    contestant_list = []
    for sortres in sortres_list:
        cont = Contestant.nodes.get(contestantid = sortres['_id'])
        contestant_list.append(cont.contestantname)

    if len(contestant_list) == 3:
        top1 = contestant_list[0]
        top2 = contestant_list[1]
        top3 = contestant_list[2]
    elif len(contestant_list) == 2:
        top1 = contestant_list[0]
        top2 = contestant_list[1]
        top3 = 'No One'
    elif len(contestant_list) == 1:
        top1 = contestant_list[0]
        top2 = 'No One'
        top3 = 'No One'
    else:
        top1 = 'No One'
        top2 = 'No One'
        top3 = 'No One'

    data = {
                'flag':True,
                'dataPoint':dataPoint,
                'top1':top1,
                'top2':top2,
                'top3':top3
            }
    return JsonResponse(data)

def statisticResult(request):
    exambatchid = request.GET.get('exambatch', None)
    stage = request.GET.get('stage', None)
    # print(exambatchid)
    exambatch = ExamBatch.nodes.get(exambatchid=exambatchid)

    definition = dict(node_class=Contestant, direction=INCOMING, relation_type=None, model=None)
    getTraversals = Traversal(exambatch, Contestant.__label__, definition)

    mydocre = mycol.find({'exambatchid':exambatchid})
    
    sortres_list = mycol.find({'exambatchid':exambatchid}).sort("result",-1).limit(3)
    full_sorlist = mycol.find({'exambatchid':exambatchid}).sort("result",-1).limit(10)
    
    contestant_list = []
    full_contestant_list =[]

    for contestant in full_sorlist:
        cont = Contestant.nodes.get(contestantid = contestant['_id'])
        full_contestant_list.append(cont.contestantname)

    full_contestant_list = full_contestant_list[3:]
    s =''
    for contestant in full_contestant_list:
        temp = '''<p style="color:red;font-weight: 900;font-size: 24pt;">'''+ contestant +'''</p>'''
        s += temp

    for sortres in sortres_list:
        cont = Contestant.nodes.get(contestantid = sortres['_id'])
        contestant_list.append(cont.contestantname)

    if len(contestant_list) == 3:
        top1 = contestant_list[0]
        top2 = contestant_list[1]
        top3 = contestant_list[2]
    elif len(contestant_list) == 2:
        top1 = contestant_list[0]
        top2 = contestant_list[1]
        top3 = 'No One'
    elif len(contestant_list) == 1:
        top1 = contestant_list[0]
        top2 = 'No One'
        top3 = 'No One'
    else:
        top1 = 'No One'
        top2 = 'No One'
        top3 = 'No One'

    #
    dataPoint = []
    chart = mycol.find({'exambatchid':exambatchid}).sort("result",1)
    order = 0
    for element in chart:
        order += 1
        cont = Contestant.nodes.get(contestantid = element['_id'])
        temp = { 'x': order, 'y': element['result'], 'label': str(cont.contestantname), 'color':"#E21B3C"}
        dataPoint.append(temp)
    
    data = {
                'flag':True,
                's': s,
                'top1':top1,
                'top2':top2,
                'top3':top3,
                'dataPoint':dataPoint,
            }
    return JsonResponse(data)