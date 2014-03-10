
from app.models import *

import random
import math

def transform_to_level(PT_PER_LVL):
    r = []
    s = 0
    for i in range(len(PT_PER_LVL)):
        s += PT_PER_LVL[i]
        r.append(s)
    return r

POINT_PER_LEVEL = [6, 12, 22, 30, 50, 80, 100, 200, 500, 800, 1200, 2000, 5000, 10000, 980000]
POINT_TO_LEVEL = transform_to_level(POINT_PER_LEVEL)
MAX_LEVEL = len(POINT_PER_LEVEL)

QUESTION_TYPES = \
    [('name', 1), \
    ('year', 1), \
    # ('college', 1), \
    ('country', 2), \
    ('major', 3), \
    ('fname', 5), \
    ('lname', 6), \
    ('roommate', 9)]

QUESTION_CONTENT = {
    'name': 'Who\'s this?',
    # 'college': 'Where does he/she live?',
    'year': 'In which year are we getting rid of him/her?',
    'country': 'Where is (s)he coming from?',
    'major': "What is (s)he studying?",
    'fname': "His/her mama calls him/her (first name)?",
    'lname': "What is this person's last name?",
    'roommate': "Who is his/her roomie?"
}

SPECIAL_QUESTION_CONTENT = \
    [('color', 2), \
    ('alcohol-type', 2), \
    ('fav-food', 2), \
    ('bring-on-island', 3), \
    ('save-house', 3), \
    ('bremen-bar', 3), \
    ('professor', 5), \
    ('number', 3), \
    ('fav-sport', 5), \
    ('fav-movie', 5), \
    ('fav-actor', 5), \
    ('fav-band', 5), \
    ('fav-song', 5), \
    ('fav-book', 5), \
    ('fav-author', 5), \
    ('fav-series', 5), \
    ('fav-game', 5), \
    ('fav-place', 7), \
    ('holiday', 10), \
    ('toy', 10), \
    ('dream-job', 10), \
    ('future-plans', 10), \
    ('life-purpose', 15)]
PROPOSE_QUESTION_POINTS = 50
TOTAL_NR_SPECIAL_QUESTIONS = len(SPECIAL_QUESTION_CONTENT)

SPECIAL_QUESTION_QUESTION = {
    'color': "What's his/her favorite color?",
    'alcohol-type': "What is his/her favorite alcohol type?",
    'fav-food': "What is his/her favorite food?",
    'bring-on-island': "What would he/she bring on a deserted island?",
    'save-house': "A house is burning, the owner can only save 1 thing, what will he/she save?",
    'bremen-bar': "What is his/her favorite bremen bar?",
    'professor': "What is his/her favorite professor at Jacobs?",
    'number': "What is his/her favorite number?",
    'fav-sport': "What is his/her favorite sport?",
    'fav-movie': "What is his/her favorite movie?",
    'fav-actor': "What is his/her favorite actor?",
    'fav-band': "What is his/her favorite band?",
    'fav-song': "What is his/her favorite song?",
    'fav-book': "What is his/her favorite book?",
    'fav-author': "What is his/her favorite author?",
    'fav-series': "What is his/her favorite TV-Show?",
    'fav-game': "What is his/her favorite game?",
    'fav-place': "What is his/her favorite place on campus?",
    'holiday': "What is his/her perfect holiday?",
    'toy': "What is his/her favorite childhood toy?",
    'dream-job': "What is his/her dream job?",
    'future-plans': "What is his/her future plans?",
    'life-purpose': "What is the purpose of life?",
}

SPECIAL_QUESTION_RESEARCH = {
    'color': "What's YOUR favorite color?",
    'alcohol-type': "What's YOUR favorite alcohol type?",
    'fav-food': "What is YOUR favorite food?",
    'bring-on-island': "What would YOU bring on a deserted island?",
    'save-house': "Your house is burning, you can only save 1 thing, what will you save?", # slal
    'bremen-bar': "What's YOUR favorite bremen bar?",
    'professor': "What's YOUR favorite professor at Jacobs?",
    'number': "What is YOUR favorite number?",
    'fav-sport': "What is YOUR favorite sport?", # sappelhoff
    'fav-movie': "What's YOUR favorite movie?",
    'fav-actor': "What's YOUR favorite actor?",
    'fav-band': "What's YOUR favorite band?",
    'fav-song': "What's YOUR favorite song?",
    'fav-book': "What's YOUR favorite book?",
    'fav-author': "What's YOUR favorite author?",
    'fav-series': "What's YOUR favorite TV-Show?", # oboychenko
    'fav-game': "What's YOUR favorite game?",
    'fav-place': "What is YOUR favorite place on campus?", # nkrueger
    'holiday': "What's YOUR perfect holiday?",
    'toy': "What's YOUR favorite childhood toy?",
    'dream-job': "What's YOUR dream job?",
    'future-plans': "What are YOUR future plans?",
    'life-purpose': "What is the purpose of life?", # kalnahas
}

YEARS = ['14', '15', '16']
YEARS_NAMES = ['Year 2014', 'Year 2015', 'Year 2016']

LEVEL_NAMES = {
    0: "No one",
    1: "Alarm sounds",
    2: "Boring 8:15 class",
    3: "Get caught jSleeping",
    4: "Fill forms @registrar",
    5: "Meatless lunch! yey!",
    6: "2:15 GenCS Quiz",
    7: "Finish Homework",
    8: "Procrastinate at Coffee Bar",
    9: "Finish stupid lab report",
    10: "Get full of Doener",
    11: "Watch Breaking Bad Finale",
    12: "Play WhoIsJack",
    13: 'Party at TOS',
    14: 'Get shitfaced',
    15: 'Jack off',
    16: 'Realize that you are still at the other side'
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

def available_special_questions(college, level):
    qs = SpecialQuestionAnswer.objects.filter(college=college)
    q_available = []
    for qtype, pts in SPECIAL_QUESTION_CONTENT:
        anss = set([ans.answer for ans in qs.filter(qtype=qtype)])
        if len(anss) >= 4:
            q_available.append( qtype )
    return q_available

def get_special_questions_showed(level):
    alpha = 1.0 * level / MAX_LEVEL
    raw_showed = (1.0 - alpha) * 1 + alpha * TOTAL_NR_SPECIAL_QUESTIONS
    return min(TOTAL_NR_SPECIAL_QUESTIONS, math.ceil(raw_showed) + 3)

def get_special_question_type(q_max_index, college):
    questions = []
    total_nr_answers = 0
    i = 0
    for qcontent in SPECIAL_QUESTION_CONTENT[0:q_max_index]:
        nr_answers = SpecialQuestionAnswer.objects.filter(college=college, qtype=qcontent[0]).count()
        if nr_answers < 3:
            continue

        total_nr_answers += nr_answers
        questions.append({
            'qtype': qcontent[0],
            'nr_answers': nr_answers,
            'index': i
        })
        i += 1
    if len(questions) == 0:
        return -1

    s = 0
    prob = random.random()
    for q in questions:
        s += q['nr_answers']
        if prob <= (1.0 * s / total_nr_answers):
            return q['index']
    return questions[len(questions)-1]['index']


def is_personal_question(level):
    alpha = 1.0 * level / MAX_LEVEL
    random_coeff = (1.0 - alpha) * 0.5 + alpha * 0.9
    return random.random() < random_coeff

def is_propose_question():
    return random.random() < (1.0 / 1000)

def should_ask_question(nr_q_ans, nr_q_avail, level):
    if nr_q_avail == 0:
        if nr_q_ans > get_special_questions_showed(4):
            # If the user answered question for level 4 already
            # and no one else is playing, stop asking questions
            return False
        # Get more answers from users
        return True
    coeff = 2
    if nr_q_ans > nr_q_avail:
        coeff += nr_q_ans - nr_q_avail
    for i in range(3):
        if level + i <= MAX_LEVEL:
            if nr_q_ans > get_special_questions_showed(level + i):
                coeff += 1

    return random.random() < (1.0 / coeff)

def create_personal_question(st, college, level):
    context = {}
    # Create personal quertion type:
    q_ans = SpecialQuestionAnswer.objects.filter(student=st)
    q_available = available_special_questions(college, level)
    if should_ask_question(len(q_ans), len(q_available), level):
        q_type_selected = ""
        answered_questions_types = [q.qtype for q in q_ans]
        unanswered_questions_types = []
        for qtype, pts in SPECIAL_QUESTION_CONTENT:
            if not qtype in answered_questions_types:
                unanswered_questions_types.append( qtype )
        for i in range(len(unanswered_questions_types)):
            if len(unanswered_questions_types) == i+1 or random.random() < 0.66:
                q_type_selected = unanswered_questions_types[i]
            if q_type_selected != "":
                break

        if q_type_selected != "":
            context['question_type'] = (q_type_selected, dict(SPECIAL_QUESTION_CONTENT)[q_type_selected])
            context['question_content'] = SPECIAL_QUESTION_RESEARCH[ q_type_selected ]
            context['question_target'] = st
    else:
        if len(q_available) > 0:
            while(True):
                q_index = get_special_question_type( int(get_special_questions_showed(level)), college )
                # q_index = random.randrange( get_special_questions_showed(level) )
                q_type_selected = SPECIAL_QUESTION_CONTENT[q_index][0]

                all_answers = [x for x in SpecialQuestionAnswer.objects.filter(college=college, qtype=q_type_selected)]
                if len(all_answers) < 3:
                    continue
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
                if len(choices) < 3:
                    continue

                context['question_type'] = (q_type_selected, dict(SPECIAL_QUESTION_CONTENT)[q_type_selected])
                context['question_content'] = SPECIAL_QUESTION_QUESTION[ q_type_selected ]
                context['question_target'] = target.student
                random.shuffle(choices)
                context['choices'] = choices
                break
    return context

def create_propose_question(st):
    context = {}
    context['question_target'] = st
    context['question_type'] = ('propose', PROPOSE_QUESTION_POINTS)
    context['question_content'] = "WOW! That was lucky! YOU can now propose a question:"
    return context

def create_question(st, college, level):
    context = {}

    if is_propose_question():
        return create_propose_question(st)

    if is_personal_question(level):
        context = create_personal_question(st, college, level)
        if context != {}:
            return context

    # Create normal question type
    allstudents = [st for st in Student.objects.filter(college=college).exclude(id=st.id)]

    rr = random.randrange( min(level, len(QUESTION_TYPES)) )
    question_type = QUESTION_TYPES[rr]

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
    if user == target and question_type == 'propose':
        return answer != None and answer != ""

    if question_type in SPECIAL_QUESTION_RESEARCH:
        if user != target:
            qans = SpecialQuestionAnswer.objects.filter(student=target, qtype=question_type)
            return (len(qans) != 0) and qans[0].answer == answer
        else:
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
    if q_type == 'propose':
        return PROPOSE_QUESTION_POINTS
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

# Arts Olympics session
# POINT_PER_LEVEL = [3, 5, 7, 15, 25, 50, 75, 150, 300, 600, 1200, 2500, 5000, 10070, 980000]
# LEVEL_NAMES = {
#     0: "No one",
#     1: "New Born",
#     2: "Pet Rock",
#     3: "Guy stuck in the elevator",
#     4: "Snoop Lion",
#     5: "Joey from friends",
#     6: "Skrillex",
#     7: "Walter White",
#     8: "Darth Vader",
#     9: "Tim Minchin",
#     10: "Charlie Chaplin",
#     11: "Quentin Tarantino",
#     12: "Bob Marley",
#     13: 'Douglas Hofstadter',
#     14: 'Leonardo da Vinci',
#     15: 'Jack',
#     16: 'Jon Lajoie'
# }