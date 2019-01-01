from django.db import models

# Create your models here.


class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    latexbody = models.TextField()
    qdate = models.DateField(null=True, blank= True)
    parent = models.IntegerField(null=True)
    difficulty = models.IntegerField()
    def __int__(self):
        return self.qid
    def getLatex(self, shuffled=False):
        output = """"""
        output += r"""\question """
        output += (self.latexbody + """\newline
""")
        embeds = Has_Embed.objects.filter(qid=self)
        if embeds != None and embeds != []:
            for embed in embeds:
                output+=(r"""\includegraphics[height=3em]{""" + str(embed.filename) + """} \newline
""")


        output+=(r"""\begin{oneparchoices}
""")
        choices = Choice.objects.filter(qid=self)
        multiFlag = 0
        order = list(range(len(choices)))
        if(shuffled==True):
            random.shuffle(order)

        for i in order:
            output+=(r"""\choice """)
            choice_embed = choices[i].embed
            if choice_embed != None and choice_embed != []:
                output+=(r"""\includegraphics[height=2em]{""" + str(choice_embed.filename) + """}
""")
            if choices[i].choicetext != "":
                output+=(choices[i].choicetext)
                output += ("""
""")
        output+=(r"""\end{oneparchoices}
""")
        for i in order:
            if choices[i].flag == 1:
                answer = i
                break
        return output, answer
    def getLatexCorrect(self, shuffled=False):
        output = """"""
        output += r"""\question """
        output += (self.latexbody + """\newline
""")
        embeds = Has_Embed.objects.filter(qid=self)
        if embeds != None and embeds != []:
            for embed in embeds:
                output+=(r"""\includegraphics[height=3em]{""" + str(embed.filename) + """} \newline
""")


        output+=(r"""\begin{oneparchoices}
""")
        choices = Choice.objects.filter(qid=self)
        multiFlag = 0
        order = list(range(len(choices)))
        if(shuffled==True):
            random.shuffle(order)

        for i in order:
            if choices[i].flag == 1:
                output+=(r"""\CorrectChoice """)
            else:
                output+=(r"""\choice """)
            choice_embed = choices[i].embed
            if choice_embed != None and choice_embed != []:
                output+=(r"""\includegraphics[height=2em]{""" + str(choice_embed.filename) + """}
""")
            if choices[i].choicetext != "":
                output+=(choices[i].choicetext)
                output += ("""
""")
        output+=(r"""\end{oneparchoices}
""")

        return output







class Embed(models.Model):
    filename = models.TextField(primary_key=True)
    def __str__(self):
        return str(self.filename)


class Choice(models.Model):
    choiceid = models.AutoField(primary_key=True)
    choicetext = models.TextField(default="DefaultChoice")
    flag = models.IntegerField()
    pos = models.TextField(null=True)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    embed = models.ForeignKey(Embed, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = (("choiceid", "qid"),)
    def __str__(self):
        return self.choicetext

class Has_Embed(models.Model):
    qid = models.ForeignKey(Question,on_delete=models.CASCADE)
    filename = models.ForeignKey(Embed, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("filename", "qid"),)
    def __str__(self):
        return str(self.filename)
    
class Topic(models.Model):
    topicname = models.TextField(primary_key=True)
    def __str__(self):
        return str(self.topicname)


class BelongsTo(models.Model):
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    topicname = models.ForeignKey(Topic, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("topicname", "qid"),)
    def __str__(self):
        return str(self.topicname)


class Choice_Embed(models.Model):
    choiceid = models.ForeignKey(Choice,on_delete=models.CASCADE)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    filename = models.ForeignKey(Embed, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("filename", "qid", "choiceid"),)



class Exam(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    q_embed = models.ForeignKey(Embed, on_delete=models.CASCADE)
    q_topic = models.ManyToManyField(Topic, related_name="topic")
    choices = models.ManyToManyField(Choice, related_name="choice")
