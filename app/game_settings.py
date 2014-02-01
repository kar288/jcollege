
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
    ('roommate', 7)]

QUESTION_CONTENT = {
    'name': 'What is the name of this person?',
    'year': 'What is the year of study of this person?',
    'country': 'What is this person country of residence?',
    'major': "What is this person's major?",
    'fname': "What is this person's first name?",
    'lname': "What is this person's last name?",
    'roommate': "Who is this person's roommate?"
}

def get_level(st):
    for level in range(len(POINT_TO_LEVEL)):
        if POINT_TO_LEVEL[level] > st.points:
            return level + 1

def create_question(st, college, level):
    context = {}
    students = Student.objects.filter(college=college)

    rr = random.randrange(level)
    question_type = QUESTION_TYPES[ rr ]
    sample = random.sample(students.exclude(id=st.id), 4)
    target = sample[0]

    context['question_type'] = question_type
    context['question_content'] = QUESTION_CONTENT[ question_type[0] ]
    context['question_target'] = target

    choices = []
    if question_type[0] == 'name':
        choices = [(t.fname + " " + t.lname) for t in sample]
    elif question_type[0] == 'year':
        choices = ['14', '15', '16']
    elif question_type[0] == 'country':
        choices = [ t.country for t in sample ]
    elif question_type[0] == 'major':
        choices = [ t.major for t in sample ]
    if choices != []:
        random.shuffle(choices)
        context['choices'] = choices

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
        return (target.fname == answer)
    elif question_type == 'lname':
        return (target.lname == answer)
    return False
