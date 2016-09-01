from codeforces import CodeforcesAPI
import random

api = CodeforcesAPI()


def solved(submission):
    if 'OK' == submission.verdict.value:
        return True
    else:
        return False


def groups(handle):
    unsolved_group = []
    solved_group = []
    submissions = api.user_status(handle)
    for sub in submissions:
        if solved(sub) and (not (sub.problem in solved_group)):
            solved_group.append(sub.problem)
    submissions = api.user_status(handle)
    for sub in submissions:
        if not (sub.problem in solved_group) and not (sub.problem in unsolved_group):
            unsolved_group.append(sub.problem)
    return [solved_group, unsolved_group]


def unsolved_group(handle):
    return groups(handle)[1]


def solved_group(handle):
    return groups(handle)[0]



## TAG GROUPS ##

posible_groups = ['', 'dp', 'constructive algorithms', 'dfs and similar', 'math', 'number theory', 'probabilities',
                  'graphs', 'brute force', 'implementation', 'data structures', 'hashing', 'string suffix structures',
                  'strings', 'sortings', 'flows', 'greedy', 'trees', 'matrices', 'binary search', 'geometry',
                  'games', 'two pointers', 'dsu', 'chinese remainder theorem', 'bitmasks', 'divide and conquer',
                  'shortest paths', 'fft']


def problem_group(subject):
    problem_group = []
    if str(subject) in posible_groups:
        formated = subject.replace(' ', '%20')
        problem_group = list(api.problemset_problems([formated])['problems'])
    return problem_group


def problem_statistics_group(subject):
    problem_statistics_group = []
    if str(subject) in posible_groups:
        formated = subject.replace(' ', '%20')
        problem_statistics_group = list(api.problemset_problems([formated])['problemStatistics'])
    return problem_statistics_group


def random_problem(subject):
    subject_group = problem_group(subject)
    if len(subject_group) >= 1:
        problem = random.choice(subject_group)
        return problem
    else:
        return False

def easiest(handle, subject=''):
    subject_group = problem_group(subject)
    if len(subject_group) < 1:
        return False
    subject_statistics_list = problem_statistics_group(subject)
    solved_list = solved_group(handle)
    subject_statistics_list = sorted(subject_statistics_list,
                                      key= lambda problem_statistics: problem_statistics.solved_count, reverse = False)
    problem_stats = None
    problem_ret = None
    for stats in subject_statistics_list:
        flag = False
        for problem in solved_list:
            if stats.index == problem.index and stats.contest_id == problem.contest_id:
                flag = True
        if flag == False:
            problem_stats = stats
    for problem in subject_group:
        if problem.index == problem_stats.index and problem.contest_id == problem_stats.contest_id:
            problem_ret = problem
    return problem_ret

