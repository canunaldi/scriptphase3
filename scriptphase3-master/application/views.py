from django.shortcuts import render
from application.models import Question,Choice,Embed,Has_Embed,Topic,BelongsTo,Choice_Embed,Exam
import datetime
import subprocess
import random
# Create your views here.


from django.http import HttpResponse, FileResponse
from .forms import NameForm
from django.core import serializers
#from reportlab.pdfgen import canvas
import io


def addquestion(request):
    return render(request, 'application/addquestion.html')
        

def index(request):
    questions = Question.objects.all()
    total = []
    for question in questions:
        total.append(question)
    context = {"questions":total}
    return render(request, 'application/index.html', context=context)

def question_detail(request):
    print(request.POST)
    if request.method == 'POST':
        qid = (request.POST['question'][:-1])
        question = Question.objects.get(qid = qid)
        if request.POST['updatebody'] != '':
            newbody = request.POST['updatebody']
            question.latexbody = newbody
            question.save()
        if request.POST['addtopic'] != '':
            topic = request.POST['addtopic']
            topic_model = None
            try:
                topic_model = Topic.objects.get(topicname = topic)
            except:
                pass
            if topic_model == None:
                topic_model = Topic(topicname = topic)
                topic_model.save()
            belonging = BelongsTo(qid = question, topicname = topic_model)
            belonging.save()
        if request.POST['deltopic'] != '':
            topic = request.POST['deltopic']
            Topic.objects.filter(topicname= topic).delete()
        if request.POST['addEmbed'] != '':
            embed = request.POST['addEmbed']
            embed_model = None
            try:
                embed_model = Embed.objects.get(filename = topic)
            except:
                pass
            if embed_model == None:
                embed_model = Embed(filename = embed)
                embed_model.save()
            has_embed = Has_Embed(qid = question, filename = embed_model)
            has_embed.save()
        if request.POST['delEmbed'] != '':
            embed = request.POST['delEmbed']
            Embed.objects.filter(filename= embed).delete()
        if request.POST['updateParent'] != '':
            newparent = request.POST['updateParent']
            question.parent = newparent
            question.save()
        if request.POST['updateAskDate'] != '':
            askdate = request.POST['updateAskDate']
            question.qdate = askdate
            question.save()
        if 'choiceyes' in request.POST:
            if request.POST.getlist('choiceid') != '':
                choiceid = request.POST.getlist('choiceid')
                print(choiceid)
               
                index = 0
                print('Buraya bascaz')
                print((request.POST))
                print('===================')
                if request.POST.getlist('choicetext') != '':
                    for choice in request.POST.getlist('choicetext'):
                        print("############")
                        print(choice)
                        if choice != "":
                            choiceideach = choiceid[index]
                            updatechoice = Choice.objects.get(choiceid = choiceideach)
                            newtext = request.POST.getlist('choicetext')[index]
                            updatechoice.choicetext = newtext
                            updatechoice.save()
                            if request.POST.getlist('choicecorrect') != '': 
                                newflag = request.POST.getlist('choicecorrect')[index]
                                updatechoice.flag = newflag
                                updatechoice.save()
                            if request.POST.getlist('choicepos') != '': 
                                newpos = request.POST.getlist('choicepos')[index]
                                updatechoice.pos =newpos
                                updatechoice.save()
                        index +=1
                    

        if 'deleteyes' in request.POST:
            Question.objects.filter(qid=qid).delete()
    return render(request, 'application/question_done.html')
    

def question(request):
    question = []
    embeds = []
    choices = []
    topics = []
    result_embed = []
    result_choice = []
    result_topic = []
    if request.method == 'POST':
        print(request.POST['question'])
        if request.POST['question'] != '':
            qid = request.POST['question']
            try:
                question = Question.objects.get(qid = qid)
            except error:
                pass
            try:
                embeds = Has_Embed.objects.filter(qid = question)
                for embed in embeds:
                    result_embed.append(embed)
            except:
                pass
            try:
                choices = Choice.objects.filter(qid = question)
                for choice in choices:
                    result_choice.append(choice)
            except:
                pass
            try:
                topics = BelongsTo.objects.filter(qid = question)
                for topic in topics:
                    print(topic)
                    result_topic.append(topic)
            except:
                pass
            
                
    print(question)
    print(result_embed)
    print(result_choice)
    print(result_topic)
    output, _ = question.getLatex()
    print(output)
    #serialized_obj = serializers.serialize('json',  list([output]) )

    
    context = {'question': question, 'embeds': result_embed, 'choices': result_choice, 'topics':result_topic, 'getter_q':output}
    return render(request, 'application/question.html', context)

            

        #form = NameForm(request.POST)
        #print(form.is_valid())
        #if form.is_valid():
        #    if 'question' in request.POST:
        #        print(form.cleaned_data['question'])
        #    if 'deneme' in request.POST:
        #        print("ANAN")


def getLatexText(iterator, shuffled=False):

		answers = []

		returnString = """\\documentclass{exam}\n\\usepackage{graphicx}\n\\begin{document}\n\\begin{questions}\n"""


		idList = []
		for item in iterator:
			idList.append(item)

		if(shuffled==True):
			random.shuffle(idList)

		for item in idList:
			temp = Question.objects.get(qid=item)
			if temp != None:
				text, answer = temp.getLatex(shuffled)
				returnString = returnString + text
				answers.append(answer)

		returnString = returnString + (r"""\end{questions}
\end{document}""")



		return returnString, answers

def getLatex(iterator, shuffled=False):
    answers = []

    with open("exam.tex", 'w') as f:
        f.write("""\\documentclass{exam}\n\\usepackage{graphicx}\n\\begin{document}\n\\begin{questions}\n""")


        idList = []
        for item in iterator:
            idList.append(item)

        if(shuffled==True):
            random.shuffle(idList)

        for item in idList:
            temp = Question.objects.get(qid=item)
            if temp != None:
                text, answer = temp.getLatex(shuffled)
                f.write(text)
                answers.append(answer)

        f.write(r"""\end{questions}
\end{document}""")
    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'exam.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()


    return answers

def qbank_detail(request):
    print(request.POST)
    if request.method == "POST":
        questions = []
        answer = []
        if "topic" in request.POST:
            topicsearch = request.POST["topicsearch"]
            valid_questions = BelongsTo.objects.filter(topicname=topicsearch)
            for question in valid_questions:
                questions.append(question.qid)
        if "difficulty" in request.POST:
            difficulty = request.POST["difficultysearch"]
            valid_questions = Question.objects.filter(difficulty = difficulty)
            for question in valid_questions:
                questions.append(question)
        if "askdate" in request.POST:
            start = request.POST["datesearchstart"]
            startarr = start.split("-")
            start = datetime.date(int(startarr[0]),int(startarr[1]),int(startarr[2]))
            end = request.POST["datesearchend"]
            endarr = end.split("-")
            end = datetime.date(int(endarr[0]),int(endarr[1]),int(endarr[2]))
            total = Question.objects.all()
            for question in total:
                if question.qdate != None and question.qdate > start and question.qdate<end:
                    questions.append(question)
        if "latex" in request.POST:
            shuffle = False
            if "shufflelatex" in request.POST:
                shuffle = True
            iterator = request.POST["getlatex"].split(",")
            answer = getLatex(iterator,shuffle)
        if "latextext" in request.POST:
            shuffle = False
            if "shufflelatextext" in request.POST:
                shuffle = True
            iterator = request.POST["getlatextext"].split(",")
            print(iterator)
            answer = getLatexText(iterator,shuffle)

        if "updatedate" in request.POST:
            questionList = request.POST["dateupdate"]
            newDate = request.POST['newdate']
            questionList = questionList.split(',')
            questionList = [int(x) for x in questionList]
            valid_questions = Question.objects.filter(qid__in  = questionList)
            for question in valid_questions:
                question.qdate = newDate
                question.save()
                print('{} id Saved.'.format(question.qid))

#            for question in valid_questions:
#                updateList.append(question.qid)

            
    print("############")
    print(questions)
    print("############")
    context = {"valid_questions":questions, "answer":answer}
    return render(request, "application/qbank_result.html", context)


def qbank(request):
    questions = Question.objects.all()
    embeds = Embed.objects.all()
    choices = Choice.objects.all()
    topics = Topic.objects.all()
    context = {'questions': questions, 'embeds': embeds, 'choices': choices, 'topics': topics}
    return render(request, "application/qbank.html",context)  


def getPDFExam(booklet,no):
		
    exam, _ = getLatexExam(booklet)

    with open("booklet" + str(no) + ".tex", 'w') as f:
        f.write(exam)

    cmd = ["pdflatex", "-interaction", "nonstopmode", "-output-directory", "temp/pdf", "booklet" + str(no) + ".tex"]
    proc = subprocess.Popen(cmd)
    proc.communicate()

    filename = "booklet" + str(no) + ".tex"

    return filename

def getLatexExam(booklet):
    returnString = """\\documentclass{exam}""" + """\n""" + """\\usepackage{graphicx}""" + """\n"""  + """ \n""" + """\\begin{document}"""\
    + """\n""" + """\\begin{questions}""" + """\n"""

    answers = []
    for element in booklet:
        question = element[0]
        text, answer = question.getLatex(shuffled=True)
        returnString+=text
        answers.append(answer)

    returnString+=r"""\end{questions}
\end{document}"""


    return returnString, answers





def getLatexKey(booklet):
    returnString = """\\documentclass{exam}""" + """\n""" + """\\usepackage{graphicx}""" + """\n""" + """\\begin{document}"""\
    + """\n""" + """\\begin{questions}""" + """\n"""

    answers = []

    exam = booklet

    for element in exam:
        question = element[0]
        text = question.getLatexCorrect(shuffled=True)
        returnString += text

    returnString += r"""\end{questions}
\end{document}"""


    return returnString

def getPDFKey(booklet,no):
    key = getLatexKey(booklet)

    with open("answerkey" + str(no) + ".tex", 'w') as f:
        f.write(key)

    cmd = ['pdflatex', '-interaction', 'nonstopmode', "answerkey" + str(no) + ".tex"]

    proc = subprocess.Popen(cmd)
    proc.communicate()

    filename = "answerkey" + str(no) + ".tex"

    return filename

def getCSVKey(booklets):
		
    mapper = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E"}

    f = open("answers.csv", 'w')
    try:
        for num, booklet in enumerate(booklets):
            f.write("Booklet " + mapper[num] + "\n\n")
            for num, element in enumerate(booklet):
                question = element[0]
                _, answer = question.getLatex()
                print("Answer: ", answer)
                f.write(str(num+1) + "," + str(mapper[answer]) + "\n")

    finally:
        f.close()

def exam_result(request):
    questions = []
    if request.method == "POST":
        print("PATATESSSS")
    if "newexam" in request.POST:
        questionList = request.POST["createexam"]
        questionList = questionList.split(',')
        questionList = [int(x) for x in questionList]
        print("questionList: {}".format(questionList))
        print("questionList type: {}".format(type(questionList)))
        valid_questions = Question.objects.filter(qid__in  = questionList)
        total = []
        for question in valid_questions:
            embeds = Has_Embed.objects.filter(qid = question)
            new_embeds=[]
            for embed in embeds:
                new_embeds = (embed.filename)
            topics = BelongsTo.objects.filter(qid = question)
            new_topics =[]
            for topic in topics:
                new_topics.append(topic.topicname)
            print(new_topics)
            q_choices = Choice.objects.filter(qid=question)
            total.append([question,new_embeds,new_topics,q_choices])
        print("####TOTAL#####")
        print(total)
#            questions.append(question.qid)
#        print("Valid question len: {}".format(len(valid_questions)))
#        resString = ""
#        for item in questions:
#            resString = resString + str(item) + ' '
        
#        message = 'New exam is created successfully. Question IDs: {}'.format(resString)
        if "shuffled" in request.POST:

            bookletNo = int(request.POST["createshuffled"])
            booklets = []
            for i in range(bookletNo):
                order = list(range(len(total)))
                random.shuffle(order)
                booklet = []
                for ra in order:
                    element = total[ra]
                    question = element[0]
                    embeds = element[1]
                    topic = element[2]
                    neworder = list(range(len(element[3])))
                    random.shuffle(neworder)
                    choices=[]
                    for ch in neworder:
                        choices.append(element[3][ch])
                    booklet.append([question,embeds,topic,choices])
                booklets.append(booklet)
            print("#####BOOKLETS####")
            print(booklets)

                    

            message = "SHUFFLE"
        if "examlatex" in request.POST:
            bookletNo = (request.POST["getexamlatex"])
            bookletNo = bookletNo.split(",")
            print(bookletNo)
            for bookleteach in bookletNo:
                bookleteach = int(bookleteach)
                message = getLatexExam(booklets[bookleteach-1])
        if "exampdf" in request.POST:
            bookletNo = (request.POST["getexampdf"])
            bookletNo = bookletNo.split(",")
            print(bookletNo)
            for bookleteach in bookletNo:
                bookleteach = int(bookleteach)
                message = getPDFExam(booklets[bookleteach-1],bookleteach-1)
        if "keylatex" in request.POST:
            bookletNo = (request.POST["getanswerlatex"])
            bookletNo = bookletNo.split(",")
            print(bookletNo)
            for bookleteach in bookletNo:
                bookleteach = int(bookleteach)
                message = getLatexKey(booklets[bookleteach-1])
        if "keypdf" in request.POST:
            bookletNo = (request.POST["getkeypdf"])
            bookletNo = bookletNo.split(",")
            print(bookletNo)
            for bookleteach in bookletNo:
                bookleteach = int(bookleteach)
                message = getPDFKey(booklets[bookleteach-1], bookleteach-1)
        if "csvkey" in request.POST:
            message = getCSVKey(booklets)
    buffer = io.BytesIO()
    context = {"valid_questions":questions, "message":message}
    return render(request, "application/exam_result.html", context)


def exam(request):
    questions = Question.objects.all()
    embeds = Embed.objects.all()
    choices = Choice.objects.all()
    topics = Topic.objects.all()

    context = {"questions":questions, "embeds":embeds, "choices":choices, "topics":topics}
    return render(request, "application/exam.html", context)

#        <label>Create a New Exam</label><input type="radio" name="newexam"/> <input type="text" name="createexam" placeholder="Enter a Question List"/><br><br>
#        <label>Create Shuffled</label><input type="radio" name="shuffled"/><input type="text" name="createshuffled" placeholder="Enter the Booklet Amount"/><br><br>
#        <label>Get Exam Latex</label><input type="radio" name="examlatex"/><input type="text" name="getexamlatex" placeholder="Enter the Booklet No For Exam Latex"/><br><br>
#        <label>Get Exam PDF</label><input type="radio" name="exampdf"/><input type="text" name="getexampdf" placeholder="Enter the Booklet No For Exam PDF"/><br><br>
#        <label>Get Answer Latex</label><input type="radio" name="keylatex"/><input type="text" name="getanswerlatex" placeholder="Enter the Booklet No For Key Latex"/><br><br>
#        <label>Get Answer PDF</label><input type="radio" name="keypdf"/><input type="text" name="getkeypdf" placeholder="Enter the Booklet No For Key PDF"/><br><br>
#        <label>Get CSV Key</label><input type="radio" name="csvkey"/><br><br>
#        <input type="submit">

#    return render(request,"application/exam.html")  
#    return FileResponse(buffer, as_attachment=True, filename=)
