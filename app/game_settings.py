
from app.models import *

import random

def transform_to_level(PT_PER_LVL):
    r = []
    s = 0
    for i in range(len(PT_PER_LVL)):
        s += PT_PER_LVL[i]
        r.append(s)
    return r

POINT_PER_LEVEL = [3, 5, 7, 15, 25, 50, 75, 150, 300, 600, 1200, 2500, 5000, 10070, 980000]
POINT_TO_LEVEL = transform_to_level(POINT_PER_LEVEL)
print POINT_TO_LEVEL

QUESTION_TYPES = \
    [('name', 1), \
    ('year', 1), \
    ('college', 1), \
    ('country', 2), \
    ('major', 3), \
    ('fname', 5), \
    ('lname', 6), \
    ('roommate', 9)]

QUESTION_CONTENT = {
    'name': 'Who\'s this?',
    'college': 'Where does he/she live?',
    'year': 'In which year are we getting rid of him/her?',
    'country': 'Where is (s)he coming from?',
    'major': "What is (s)he studying?",
    'fname': "His/her mama calls him/her (first name)?",
    'lname': "What is this person's last name?",
    'roommate': "Who is his/her roomie?"
}

YEARS = ['14', '15', '16']
YEARS_NAMES = ['Year 2014', 'Year 2015', 'Year 2016']

LEVEL_NAMES = {
    0: "No one",
    1: "New Born",
    2: "Pet Rock",
    3: "Guy stuck in the elevator",
    4: "Snoop Lion",
    5: "Joey from friends",
    6: "Skrillex",
    7: "Walter White",
    8: "Darth Vader",
    9: "Tim Minchin",
    10: "Quentin Tarantino",
    11: "Bob Marley",
    12: 'Douglas Hofstadter',
    13: 'Leonardo da Vinci',
    14: 'Jack',
    15: 'Jon Lajoie'
}

def get_level(st):
    for level in range(len(POINT_TO_LEVEL)):
        if POINT_TO_LEVEL[level] > st.points:
            return [level + 1, LEVEL_NAMES[level+1]]
    level = len(POINT_TO_LEVEL)
    return [level, LEVEL_NAMES[level]]

def get_progress(st):
    level = get_level(st)[0]
    if level <= len(POINT_PER_LEVEL):
        if level <= 1:
            level_before = 0
        else:
            level_before = POINT_TO_LEVEL[level-2]
        level_after = POINT_TO_LEVEL[level-1]
        current_pts = st.points
        return ((current_pts-level_before+0.0)/(level_after-level_before+0.0)*100.0)
    else:
        return 100

def create_question(st, college, level):
    context = {}
    # students = Student.objects.filter(college=college)
    students = Student.objects.all()

    rr = random.randrange(level)
    question_type = QUESTION_TYPES[ min([rr, len(QUESTION_TYPES)-1]) ]
    allstudents = [st for st in students.exclude(id=st.id)]
    random.shuffle(allstudents)
    target = None

    choices = []
    if question_type[0] == 'name':
        target = allstudents[0]
        choices = [(t.fname + " " + t.lname) for t in allstudents[0:4]]
    elif question_type[0] == 'college':
        target = allstudents[0]
        choices = ['Mercator', 'Nordmetall', 'College-III', 'Krupp']
    elif question_type[0] == 'year':
        for t in allstudents:
            if t.year in YEARS:
                target = t
                break
        choices = YEARS_NAMES
    elif question_type[0] == 'country':
        target = allstudents[0]
        choices = []
        for t in allstudents:
            if not t.country in choices:
                choices.append( t.country )
                if len(choices) == 4:
                    break
    elif question_type[0] == 'major':
        choices = []
        for t in allstudents:
            if t.major != "" and not t.major in choices:
                if target == None:
                    target = t
                choices.append( t.major )
                if len(choices) == 4:
                    break
    elif question_type[0] == 'roommate':
        choices = []
        addnow = False
        for t in allstudents:
            if addnow:
                if not (t.fname + " " + t.lname) in choices:
                    choices.append(t.fname + " " + t.lname)
                if len(choices) == 4:
                    break
                else:
                    continue
            if t.room != "":
                fpart = t.room[0:3]
                roomnr = int(t.room[3:])
                lookfor1 = fpart + str(roomnr - 1)
                lookfor2 = fpart + str(roomnr + 1)
                roommates = Student.objects.filter(room=lookfor1) | Student.objects.filter(room=lookfor2)
                if len(roommates) > 0:
                    if target == None:
                        target = t
                        choices.append(roommates[0].fname + " " + roommates[0].lname)
                        addnow = True
    else:
        target = allstudents[0]
    if choices != []:
        random.shuffle(choices)
        context['choices'] = choices

    context['question_type'] = question_type
    context['question_content'] = QUESTION_CONTENT[ question_type[0] ]
    context['question_target'] = target

    return context

def verify_question(user, target, question_type, answer):
    if question_type == 'name':
        return (target.fname + " " + target.lname == answer)
    elif question_type == 'college':
        return (target.college == answer[0])
    elif question_type == 'year':
        return ("Year 20" + target.year == answer)
    elif question_type == 'country':
        return (target.country == answer)
    elif question_type == 'major':
        return (target.major == answer)
    elif question_type == 'fname':
        return answer in target.fname.split(' ')
    elif question_type == 'lname':
        return answer in target.lname.split(' ')
    elif question_type == 'roommate':
        names = answer.split(" ")
        useranswer = None
        for st in Student.objects.all():
            thisisit = True
            for name in names:
                thisisit = thisisit and (name in st.fname or name in st.lname)
            if thisisit:
                useranswer = st
                break
        if useranswer == None:
            return False
        return abs(int(useranswer.room[3:]) - int(target.room[3:])) == 1
    return False


# OLD GAME Settings:

# February session
# POINT_PER_LEVEL = [3, 5, 10, 25, 50, 75, 150, 300, 600, 1000000]
# LEVEL_NAMES = {
#     0: "No one",
#     1: "New Born",
#     2: "Auslander",
#     3: "Peitgen",
#     4: "Lafayettee",
#     5: "Appetito Chef",
#     6: "Nordie",
#     7: "'Hey, use jCourse'",
#     8: "TOS Bartender",
#     9: "College Master",
#     10: "Jack",
#     11: 'Andrei Militaru'
# }