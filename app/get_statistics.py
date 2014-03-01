
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

def get_popular_colleges():
    try:
        top_rank = TopRankings.objects.latest('at_time')
    except:
        return []

    college_stats = []
    for college_rank in top_rank.colleges.all():
        if college_rank.total_questions > 0:
            college_stats.append({
                'name': dict(COLLEGES)[ college_rank.college.name ],
                'stats': str(college_rank.correctly_answered) + "/" + str(college_rank.total_questions),
                'rank': college_rank.rank
            })
    return sorted(college_stats,key=lambda x:x['rank'])

def get_popular_users():
    try:
        top_rank = TopRankings.objects.latest('at_time')
    except:
        return []

    student_stats = []
    for student_rank in top_rank.students.all():
        if student_rank.total_questions > 0:
            student_stats.append({
                'student': student_rank.student,
                'stats': str(student_rank.correctly_answered) + "/" + str(student_rank.total_questions),
                'rank': student_rank.rank
            })
    return sorted(student_stats,key=lambda x:x['rank'])

def remake_popular_colleges(ranking, players):
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

    # print college_popularity
    # for stats in list(college_popularity):
    #     print stats[''], stats['total_questions'] - stats['correctly_answered']
    college_popularity = sorted(list(college_popularity.iteritems()),
        key=lambda stats:confidence(stats[1]['correctly_answered'], stats[1]['total_questions'] - stats[1]['correctly_answered']),
        reverse=True)

    college_stats = []
    r = 1
    for college_name, stats in college_popularity:
        if stats['total_questions'] > 0:
            top_college = TopCollege(college=College.objects.get(name=college_name),
                rank=r,
                correctly_answered=stats['correctly_answered'],
                total_questions=stats['total_questions'])
            top_college.save()
            ranking.colleges.add(top_college)
            r += 1

def remake_popular_users(ranking, players):
    pop_studs = sorted(players,key=lambda x:confidence(x.correctly_answered, x.total_questions - x.correctly_answered), reverse=True)
    pop_list = []
    r = 1
    for p in pop_studs[:5]:
        if p.total_questions > 0:
            top_student = TopStudent(student=p.stud,
                rank=r,
                correctly_answered=p.correctly_answered,
                total_questions=p.total_questions)
            top_student.save()
            ranking.students.add(top_student)
            r += 1

def remake_popularity():
    popularities = Popularity.objects.all()

    top_ranks = TopRankings()
    top_ranks.save()
    remake_popular_users(top_ranks, popularities)
    remake_popular_colleges(top_ranks, popularities)