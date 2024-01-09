import names
import json
import random
import decimal
from alive_progress import alive_bar
import time
from pathlib import Path

with open("config.json", "r" ,encoding="utf8") as f:
            config = json.load(f)

if not Path("student_data.json").is_file():
    f = open("student_data.json",'x')
    f.write('{"owner":{},"studentdata":{}}')
    f.close()

amount = {}
for level in config["Mattayom"]:
    p = int(input(f"จำนวนคนของชั้น {level} : "))
    amount.update({level:p})

def score(skill,pool): #skill level 1 2 3 4
    score = []
    for i in range(len(pool)):
        if skill == 1:
            score.append(random.randint(50,70))
        elif skill == 2:
            score.append(random.randint(60,80))
        elif skill == 3:
            score.append(random.randint(70,90))
        elif skill == 4:
            score.append(random.randint(80,100))    
        else:
            score.append(random.randint(50,70))  
    return score

def get_grade(point): #convert point to grade
    if point >= 80 and point <= 100:
        grade = 4
    elif point >= 75 and point <= 79:
        grade = 3.5
    elif point >= 70 and point <= 74:
        grade = 3
    elif point >= 65 and point <= 69:
        grade = 2.5
    elif point >= 60 and point <= 64:
        grade = 2
    else:
        grade = 1
    return grade

def get_avg_weighted(mark,weight): #To calculate avarage
    grade = list(map(get_grade,mark))
    wx = sum(map(lambda x,y: x * y,grade,weight))
    result = wx/sum(weight)
    return '%.2f' % trueRound(result,2)

def get_sum_weight():
    summare = 0
    for basic in basic_subject_pool:
        summare += float(basic_subject_pool[basic]["weight"])
    for addition in additional_subject_pool:
        summare += float(additional_subject_pool[addition]["weight"])
    return summare

def trueRound(num, decimalPlaces):
        a = decimal.Decimal(str(num))
        places_str = "0."
        for i in range(decimalPlaces - 1):
            places_str += "0"
        places_str += "1"
        PLACES = decimal.Decimal(places_str)
        result = a.quantize(PLACES)
        return float(result)

time_person = []

with open("student_data.json", "r" ,encoding="utf8") as f:
    database = json.load(f)
with alive_bar(total=sum([amount[m] for m in amount]),title=f'In process...',ctrl_c=False,dual_line=True) as bar:
    bar.text(f'Initializing')
    for level in config["Mattayom"]:
        for i in range(amount[level]):
            start = time.time()
            bar.text(f'Simulating Matthayom {level} creating common information')
            gender = random.choice(('male', 'female'))
            skill = random.randint(1,4)
            room = f"{level}/{random.randint(1,7)}"
            birth:str = f"{str(random.randint(1,31)).zfill(2)}/{str(random.randint(1,12)).zfill(2)}/{random.randint(48,49)}"
            code = f"{str(len(database['studentdata'])+1).zfill(5)}-{birth.replace('/','')}"
            new = {code: {
                        "name-surname":names.get_full_name(gender=gender),
                        "nickname":names.get_first_name(gender=gender),
                        "age":random.randint(15,18),
                        "birthday":birth,
                        "class":room,
                        "skill":skill,
                        "is_owned":False,
                        "school-record":{}
                }
            }
            bar.text(f'Simulating Matthayom {level} successfully creating common information')
            gpax_mark = []
            gpax_weight = []
            for term in range(1,3):
                bar.text(f'Simulating Matthayom {level} creating semaster {term}')
                gpa_weight = []
                t = {term: {"GPA":0,"GPAX":0,"basic":{},"additional":{}}}
                basic_subject_pool = config["Mattayom"][level][str(term)]["basic_subject_pool"]
                additional_subject_pool = config["Mattayom"][level][str(term)]["additional_subject_pool"]
                mark = score(skill,basic_subject_pool)
                mark2 = score(skill,additional_subject_pool)
                gpax_mark.extend(mark+mark2)
                bar.text(f'Simulating Matthayom {level} assigning basic subject')
                for basic,index in zip(basic_subject_pool,range(len(basic_subject_pool))):
                    basic_subject_pool[basic].update({ 
                        "weight":str(basic_subject_pool[basic]["weight"]),
                        "get":str(mark[index]),
                        "grade":str(get_grade(int(mark[index])))})
                    t[term]["basic"].update({basic:basic_subject_pool[basic]})   
                    gpax_weight.append(float(basic_subject_pool[basic]["weight"]))
                    gpa_weight.append(float(basic_subject_pool[basic]["weight"]))
                bar.text(f'Simulating Matthayom {level} successfully assign basic subject')

                bar.text(f'Simulating Matthayom {level} starting assign additional subject')
                for additional,index in zip(additional_subject_pool,range(len(additional_subject_pool))):
                    additional_subject_pool[additional].update({ 
                        "weight":str(additional_subject_pool[additional]["weight"]),
                        "get":str(mark2[index]),
                        "grade":str(get_grade(int(mark2[index])))})
                    t[term]["additional"].update({additional:additional_subject_pool[additional]})
                    gpax_weight.append(float(additional_subject_pool[additional]["weight"]))
                    gpa_weight.append(float(additional_subject_pool[additional]["weight"]))
                bar.text(f'Simulating Matthayom {level} successfully assign additional subject')

                bar.text(f'Simulating Matthayom {level} successfully create all semaster')
                t[term]["GPA"] = get_avg_weighted(mark+mark2,gpa_weight)
                t[term]["GPAX"] = get_avg_weighted(gpax_mark,gpax_weight)
                new[code]["school-record"].update(t)
                bar.text(f'Simulating Matthayom {level} successfully create semaster{term}')          
            database["studentdata"].update(new)
            end = time.time()
            time_person.append(end-start)
            bar.text(f'Simulating Matthayom {level} successfully dump file')
            bar()
    bar.text(f'Successful simulate all student')
with open("student_data.json", "w" ,encoding="utf8") as f:
    json.dump(database,f,ensure_ascii=False,indent=4)
print(f"Avg. time per person is {sum(time_person)/sum([amount[m] for m in amount])}")