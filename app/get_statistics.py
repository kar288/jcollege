
from app.models import *
from math import sqrt

def get_top_players():
    players = Student.objects.filter(points__gt=0)
    return sorted(players,key=lambda x:x.points, reverse=True)[:5]

def get_top_colleges():
    colleges = sorted(College.objects.all(),key=lambda x:x.points, reverse=True)
    lst = []
    for c in colleges:
        lst.append({
            'name': dict(COLLEGES)[c.name],
            'points': c.points
        })
    return lst

def _confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0
    z = 1.0 #1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)


def get_popular_users(players):
    pop_studs = sorted(players,key=lambda x:confidence(x.correctly_answered, x.total_questions - x.correctly_answered), reverse=True)
    pop_list = []
    for p in pop_studs[:5]:
        pop_list.append({
            'student': p.stud,
            'stats': str(p.correctly_answered) + "/" + str(p.total_questions)
        })
    return pop_list

def get_popular_colleges(players):
    college_popularity = {
        'M': {
            'correctly_answered': 0,
            'total_questions': 0
        },
        'N': {
            'correctly_answered': 0,
            'total_questions': 0
        },
        'K': {
            'correctly_answered': 0,
            'total_questions': 0
        },
        'C': {
            'correctly_answered': 0,
            'total_questions': 0
        }
    }
    for player in players:
        college_popularity[ player.stud.college ][ 'correctly_answered' ] += player.correctly_answered
        college_popularity[ player.stud.college ][ 'total_questions' ] += player.total_questions

    college_stats = []
    for college_name, stats in college_popularity.iteritems():
        if stats['total_questions'] > 0:
            college_stats.append({
                'name': dict(COLLEGES)[college_name],
                'stats': str(stats['correctly_answered']) + "/" + str(stats['total_questions']),
                'confidence': confidence(stats['correctly_answered'], stats['total_questions'] - stats['correctly_answered'])
            })

    return sorted(college_stats,key=lambda x:x['confidence'], reverse=True)
