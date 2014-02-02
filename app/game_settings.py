
from app.models import *

import random

def transform_to_level(PT_PER_LVL):
    r = []
    s = 0
    for i in range(len(PT_PER_LVL)):
        s += PT_PER_LVL[i]
        r.append(s)
    return r

POINT_PER_LEVEL = [3, 5, 10, 25, 50, 75, 150]
POINT_TO_LEVEL = transform_to_level(POINT_PER_LEVEL)

QUESTION_TYPES = \
    [('name', 1), \
    ('year', 1), \
    ('country', 2), \
    ('major', 3), \
    ('fname', 5), \
    ('lname', 5), \
    ('roommate', 8)]

QUESTION_CONTENT = {
    'name': 'What is the name of this person?',
    'year': 'What is the year of study of this person?',
    'country': 'What is this person country of residence?',
    'major': "What is this person's major?",
    'fname': "What is this person's first name?",
    'lname': "What is this person's last name?",
    'roommate': "Who is this person's roommate?"
}

YEARS = ['14', '15', '16']

def get_level(st):
    for level in range(len(POINT_TO_LEVEL)):
        if POINT_TO_LEVEL[level] > st.points:
            return level + 1
    return len(POINT_TO_LEVEL)

def get_progress(st):
    level = get_level(st)
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

def get_top_players(student):
    col_of_student = student.college
    players = Student.objects.filter(points__gt=0)
    return sorted(players,key=lambda x:x.points, reverse=True)[:5]


def create_question(st, college, level):
    context = {}
    students = Student.objects.filter(college=college)

    rr = random.randrange(level)
    question_type = QUESTION_TYPES[ rr ]
    allstudents = [st for st in students.exclude(id=st.id)]
    random.shuffle(allstudents)
    target = None

    choices = []
    if question_type[0] == 'name':
        target = allstudents[0]
        choices = [(t.fname + " " + t.lname) for t in allstudents[0:4]]
    elif question_type[0] == 'year':
        for t in allstudents:
            if t.year in YEARS:
                target = t
                break
        choices = YEARS
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
    elif question_type == 'year':
        return (target.year == answer)
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
