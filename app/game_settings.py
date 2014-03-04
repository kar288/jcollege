
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
MAX_LEVEL = len(POINT_PER_LEVEL)

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

SPECIAL_QUESTION_CONTENT = \
    [('color', 2), \
    ('bring-on-island', 3), \
    ('alcohol-type', 2), \
    ('fav-food', 2), \
    ('bremen-bar', 3), \
    ('professor', 5), \
    ('fav-movie', 5), \
    ('fav-actor', 5), \
    ('fav-band', 5), \
    ('fav-song', 5), \
    ('fav-book', 5), \
    ('fav-author', 5), \
    ('fav-game', 5), \
    ('holiday', 10), \
    ('toy', 10), \
    ('dream-job', 10), \
    ('future-plans', 10)]

SPECIAL_QUESTION_QUESTION = {
    'color': "What's his/her favorite color?",
    'bring-on-island': "What would he/she bring on a deserted island?",
    'alcohol-type': "What is his/her favorite alcohol type?",
    'fav-food': "What is his/her favorite food?",
    'bremen-bar': "What is his/her favorite bremen bar?",
    'professor': "What is his/her favorite professor at Jacobs?",
    'fav-movie': "What is his/her favorite movie?",
    'fav-actor': "What is his/her favorite actor?",
    'fav-band': "What is his/her favorite band?",
    'fav-song': "What is his/her favorite song?",
    'fav-book': "What is his/her favorite book?",
    'fav-author': "What is his/her favorite author?",
    'fav-game': "What is his/her favorite game?",
    'holiday': "What is his/her perfect holiday?",
    'toy': "What is his/her favorite childhood toy?",
    'dream-job': "What is his/her dream job?",
    'future-plans': "What is his/her future plans?",
}

SPECIAL_QUESTION_RESEARCH = {
    'color': "What's YOUR favorite color?",
    'bring-on-island': "What would YOU bring on a deserted island?",
    'alcohol-type': "What's YOUR favorite alcohol type?",
    'fav-food': "What is YOUR favorite food?",
    'bremen-bar': "What's YOUR favorite bremen bar?",
    'professor': "What's YOUR favorite professor at Jacobs?",
    'fav-movie': "What's YOUR favorite movie?",
    'fav-actor': "What's YOUR favorite actor?",
    'fav-band': "What's YOUR favorite band?",
    'fav-song': "What's YOUR favorite song?",
    'fav-book': "What's YOUR favorite book?",
    'fav-author': "What's YOUR favorite author?",
    'fav-game': "What's YOUR favorite game?",
    'holiday': "What's YOUR perfect holiday?",
    'toy': "What's YOUR favorite childhood toy?",
    'dream-job': "What's YOUR dream job?",
    'future-plans': "What's YOUR future plans?",
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
    10: "Charlie Chaplin",
    11: "Quentin Tarantino",
    12: "Bob Marley",
    13: 'Douglas Hofstadter',
    14: 'Leonardo da Vinci',
    15: 'Jack',
    16: 'Jon Lajoie'
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

def ask_question(nr_q_ans, level):
    if level <= 1:
        return False
    return random.random() < (1.0 / (nr_q_ans + 3 * (level-1) / 2))

def available_special_questions(college, level):
    qs = SpecialQuestionAnswer.objects.filter(college=college)
    q_available = []
    for qtype, pts in SPECIAL_QUESTION_CONTENT:
        anss = set([ans.answer for ans in qs.filter(qtype=qtype)])
        if len(anss) >= 4:
            q_available.append( qtype )
    return q_available


def create_question(st, college, level):
    context = {}

    personal = random.random() < 0.5

    if personal:
        # Create personal quertion type:
        q_ans = SpecialQuestionAnswer.objects.filter(student=st)
        if ask_question(len(q_ans), level):
            q_type_selected = ""
            answered_questions_types = [q.qtype for q in q_ans]
            unanswered_questions_types = []
            for qtype, pts in SPECIAL_QUESTION_CONTENT:
                if not qtype in answered_questions_types:
                    unanswered_questions_types.append( qtype )
            for i in range(len(unanswered_questions_types)):
                if len(unanswered_questions_types) == i+1 or random.random() < 0.5:
                    q_type_selected = unanswered_questions_types[i]
                if q_type_selected != "":
                    break

            if q_type_selected != "":
                context['question_type'] = (q_type_selected, dict(SPECIAL_QUESTION_CONTENT)[q_type_selected])
                context['question_content'] = SPECIAL_QUESTION_RESEARCH[ q_type_selected ]
                context['question_target'] = st
                return context
        else:
            q_available = available_special_questions(college, level)
            if len(q_available) > 0:
                q_index = random.randrange(min(int(level*1.5), len(q_available)))
                q_type_selected = SPECIAL_QUESTION_CONTENT[q_index][0]

                all_answers = SpecialQuestionAnswer.objects.filter(college=college, qtype=q_type_selected)
                random.shuffle(all_answers)

                target = all_answers[0]
                if target.student == st:
                    target = all_answers[1]
                choices = [target.answer]
                for ans in all_answers[1:]:
                    if not ans.answer in choices:
                        choices.append(ans.answer)
                    if len(choices) == 4:
                        break

                context['question_type'] = (q_type_selected, dict(SPECIAL_QUESTION_CONTENT)[q_type_selected])
                context['question_content'] = SPECIAL_QUESTION_QUESTION[ q_type_selected ]
                context['question_target'] = target.student
                context['choices'] = choices
                return context

    # Create normal question type
    allstudents = [st for st in Student.objects.filter(college=college).exclude(id=st.id)]

    rr = random.randrange(level)
    question_type = QUESTION_TYPES[ min([rr, len(QUESTION_TYPES)-1]) ]

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
    print user, target, question_type, answer
    if user == target and question_type in SPECIAL_QUESTION_RESEARCH:
        qans = SpecialQuestionAnswer.objects.filter(student=user, qtype=question_type)
        if len(qans) == 0:
            ans = SpecialQuestionAnswer(student=user, qtype=question_type, answer=answer, college=user.college)
            ans.save()
        else:
            raise RuntimeError
        return True


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

def get_added_points(q_type):
    if q_type in dict(QUESTION_TYPES):
        return dict(QUESTION_TYPES)[ q_type ]
    if q_type in dict(SPECIAL_QUESTION_CONTENT):
        return dict(SPECIAL_QUESTION_CONTENT)[ q_type ]
    return 0

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