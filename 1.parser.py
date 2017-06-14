import os
from bs4 import BeautifulSoup
import re
import csv

class Experience:
    def __init__(self,org,title,start_time,end_time,month:int):
        self.org=org
        self.start_time=start_time
        self.end_time=end_time
        self.title=title
        self.month=month
class Education:
    def __init__(self,org,deg,start_time,end_time,year:int):
        self.org = org
        self.start_time = start_time
        self.end_time = end_time
        self.deg = deg
        self.year = year
    def age(self,cur_year):
        if(start_time!='?'):
            return cur_year-int(start_time)
        else:
            return -1
path='doneHTML'
# count=0
csvfile=open('1parsed.csv', 'w', newline='',errors='ignore')
spamwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
for file in os.listdir(path):
    cur_file=os.path.join(path,file)
    f=open(cur_file,"rb")
    soup=BeautifulSoup(f)
    top_card=soup.find("div",{"id":"top-card"})
    try:
        name=top_card.find("span",{"class":"full-name"})
    except:
        print(cur_file)
        continue
    if(not name):
        name='?'
    elif(not isinstance(name,str)):
        name=name.text#get name
    location=top_card.find("span",{"class":"locality"})
    if (not location):
        location='?'
    else:
        location=location.text#get location
    industry=top_card.find("dd",{"class":"industry"})
    if (not industry):
        industry='?'
    else:
        industry=industry.text  # get industry
    bg_exp=soup.find("div",{"id":"background-experience"})
    experience=[]
    #get experiences#
    for cur_exp in bg_exp.find_all("div",{"class":""}):
        head=cur_exp.find("header")
        title=head.find("h4",{"class":""}).text
        company=head.find("h5",{"class":""}).text
        date_locale=cur_exp.find("span",{"class":"experience-date-locale"})
        time=date_locale.find_all("time")
        if(len(time)==1):
            start_time=time[0].text
            end_time=""
        elif(not time):
            start_time='?'
            end_time="?"
        else:
            start_time=time[0].text
            end_time=time[1].text
        long=date_locale.text
        long_str=long[long.find('(')+1:long.find(')')]
        long_year=re.search("[0-9]*(?= year)",long_str)
        if(long_year and long_year.group(0)):
            long_year=long_year.group(0)
        else:
            long_year=0
        long_month = re.search("[0-9]*(?= month)", long_str)
        if(long_month and long_month.group(0)):
            long_month=long_month.group(0)
        else:
            long_month=0
        long=int(long_year)*12+int(long_month)
        experience.append(Experience(company,title,start_time,end_time,long))
        
    bg_edu=soup.find("div",{"id":"background-education"})
    education=[]
    #get educations#
    if(bg_edu):
        for cur_edu in bg_edu.find_all("div",{"class":"editable-item section-item"}):
            head=cur_edu.find("header")
            school=head.find("h4").text
            degree=head.find("h5").text
            date=cur_edu.find("span",{"class":"education-date"})
            time=date.find_all("time")
            if(len(time)==1):
                start_time=re.search("[0-9]+",time[0].text).group(0)
                end_time=""
                long = 2016-int(start_time)
            elif(not time):
                start_time='?'
                end_time="?"
                long=-1
            else:
                start_time=re.search("[0-9]+",time[0].text).group(0)
                end_time=re.search("[0-9]+",time[1].text.strip(" – ")).group(0)
                long=int(end_time)-int(start_time)
            education.append(Education(school,degree,start_time,end_time,long))
    bg_skill=soup.find("ul",{"class":"skills-section compact-view"})
    skill=""
    if(bg_skill):
        for cur_sk in bg_skill.find_all("span",{"class":"endorse-item-name"}):
            skill+=(cur_sk.text+',')
        skill=skill[:-1]
    if(education):
        list_row=[name,location,industry,skill,education[-1].age(2016),education[0].deg,education[0].org]
    else:
        list_row=[name, location, industry, skill, '?','?','?']
    if(len(experience)<6):
        count_exp=len(experience)
    else:
        count_exp=6
    for i in range(6):
        if(i<count_exp):
            exp=experience[count_exp-1-i]
            list_row+=[exp.org,exp.month,exp.start_time,exp.title]
        else:
            list_row+=['','','','']
    spamwriter.writerow(list_row)
    # count+=1
    # if(count>=10):
    #     break