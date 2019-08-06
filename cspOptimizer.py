import itertools
import sys

from cspConsistency import *
from cspProblem     import *
from searchGeneric  import *
from searchProblem  import *

# List of valid days and times
days_list = ["mon", "tue", "wed", "thu", "fri"]
time_list = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"]

# Map days and times to numerical values ranging
# from [0-4] days and [0-7] for times
days_dict = dict(zip(days_list, range(len(days_list))))
time_dict = dict(zip(time_list, range(len(time_list))))

# Create a set of (day , time) tuples
day_time_domain = set(list(itertools.product(days_list, time_list)))

# //-------------------- // BINARY CONSTRAINTS // -------------------- //

def b_before(m1, m2):
    if (days_dict[getDayFromString(m1)] < days_dict[getDayFromString(m2)]):
        return True
    elif (days_dict[getDayFromString(m1)] == days_dict[getDayFromString(m1)]):
        if (time_dict[getTimeFromString(m1)] < time_dict[getTimeFromString(m2)]):
            return True
        else:
            return False


def b_same_day(m1, m2):
    if (days_dict[getDayFromString(m1)] == days_dict[getDayFromString(m2)]):
        return True
    else:
        return False


def b_one_day_between(m1, m2):
    if (abs(days_dict[getDayFromString(m1)] - days_dict[getDayFromString(m2)]) == 2):
        return True
    else:
        return False


def b_one_hour_between(m1, m2):
    m1_time = getTimeFromString(m1)
    m2_time = getTimeFromString(m2)
    if (abs(time_dict[m1_time] - time_dict[m2_time]) == 2):
        return True
    else:
        return False


# Dict mapping of binary constraints to their corresponding functions
b_constraints = {
    "before": b_before,
    "same-day": b_same_day,
    "one-day-between": b_one_day_between,
    "one-hour-between": b_one_hour_between
}


# //-------------------- // ---------------- // -------------------- //

# //-------------------- // HARD CONSTRAINTS // -------------------- //

def h_day(day):
    def day_equal(d):
        return getDayFromString(d) == day

    return day_equal


def h_time(time):
    def time_equal(t):
        return getTimeFromString(t) == time

    return time_equal


def h_range(s1, s2):

    s1_day = getDayFromString(s1)
    s1_time = time_dict[getTimeFromString(s1)]
    s1_day_index = days_dict[getDayFromString(s1)]

    s2_day = getDayFromString(s2)
    s2_time = time_dict[getTimeFromString(s2)]
    s2_day_index = days_dict[getDayFromString(s2)]

    def day_range(r):

        r_day = getDayFromString(r)
        r_time = time_dict[getTimeFromString(r)]
        r_day_index = days_dict[getDayFromString(r)]

        # If the day is either the start day or the end day, it automatically
        # satisfies the day range, then we check to see if the time range
        # is satisfied
        if (s1_day_index > s2_day_index):
            return False
        if (r_day == s1_day):
            if (r_time >= s1_time):
                return True
            else:
                return False
        elif (r_day == s2_day):
            if (r_time <= s2_time):
                return True
            else:
                return False
        # If the day is in between the date range,
        # the criteria is satisfied
        elif (r_day_index >= s1_day_index and r_day_index <= s2_day_index):
            return True
        else:
            return False

    return day_range


def h_morning():
    def morning(t):
        return time_dict[getTimeFromString(t)] <= time_dict['11am']

    return morning


def h_afternoon():
    def afternoon(t):
        return time_dict[getTimeFromString(t)] >= time_dict['12pm']

    return afternoon


def h_before_day(day):
    def before_day(d):
        if (days_dict[getDayFromString(d)] < days_dict[getDayFromString(day)]):
            return True
        else:
            return False

    return before_day


def h_before_time(time):
    def before_time(t):
        if (time_dict[getTimeFromString(t)] < time_dict[getTimeFromString(time)]):
            return True
        else:
            return False

    return before_time


def h_before_day_time(s):
    def before_day_time(dt):
        if (days_dict[getDayFromString(dt)] < days_dict[getDayFromString(s)]):
            if (time_dict[getTimeFromString(dt)] < time_dict[getTimeFromString(s)]):
                return True
            else:
                return False
        else:
            return False

    return before_day_time


def h_after_day(day):
    def after_day(d):
        if (days_dict[getDayFromString(d)] > days_dict[getDayFromString(day)]):
            return True
        else:
            return False

    return after_day


def h_after_time(time):
    def after_time(t):
        if (time_dict[getTimeFromString(t)] > time_dict[getTimeFromString(time)]):
            return True
        else:
            return False

    return after_time


def h_after_day_time(s):
    def after_day_time(dt):
        if (days_dict[getDayFromString(dt)] > days_dict[getDayFromString(s)]):
            if (time_dict[getTimeFromString(dt)] > time_dict[getTimeFromString(s)]):
                return True
            else:
                return False
        else:
            return False

    return after_day_time


# Dict mapping of hard constraints to their functions
h_constriants = {
    "day": h_day,
    "time": h_time,
    "day-range": h_range,
    "morning": h_morning,
    "afternoon": h_afternoon,
    "before_day": h_before_day,
    "before_time": h_before_time,
    "after_day": h_after_day,
    "after_time": h_after_time,
    "before_day_time": h_before_day_time,
    "after_day_time": h_after_day_time
}


# //-------------------- // ------------------- // -------------------- //

# //-------------------- //   SOFT CONSTRAINTS // --------------------- //

def s_early_week():
    def early_week(d):
        return abs(days_dict[getDayFromString(d)] - days_dict['mon'])

    return early_week


def s_late_week():
    def late_week(d):
        return abs(days_dict[getDayFromString(d)] - days_dict['fri'])

    return late_week


def s_early_morning():
    def early_morning(t):
        return abs(time_dict[getTimeFromString(t)] - time_dict['9am'])

    return early_morning


def s_midday():
    def midday(t):
        return abs(time_dict[getTimeFromString(t)] - time_dict['12pm'])

    return midday


def s_late_afternoon():
    def late_afternoon(t):
        return abs(time_dict[getTimeFromString(t)] - time_dict['4pm'])

    return late_afternoon


# Dict mapping of soft constraints to their corresponding functions
s_constraints = {
    "early-week": s_early_week,
    "late-week": s_late_week,
    "early-morning": s_early_morning,
    "midday": s_midday,
    "late-afternoon": s_late_afternoon
}


def getDayFromString(variable):
    return variable[0]


def getTimeFromString(variable):
    return variable[1]


# //-------------------- // ------------------- // -------------------- //

class CostCSP(CSP):

    def __init__(self, domains, constriants, soft_constraints):
        super().__init__(domains, constraints)
        self.soft_constraints = soft_constraints
        self.var_to_soft_const = {var: set() for var in self.variables}
        for con in soft_constraints:
            for var in con.scope:
                self.var_to_soft_const[var].add(con)

    def cost(self, var, value):
        sum = 0
        for con in self.var_to_soft_const[var]:
            sum += con.condition(value)
        return sum


class AStarModified(Searcher):

    def __init__(self, problem):
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierPQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self, path):
        """add path to the frontier with the appropriate cost"""

        # Removed initial
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)


class Search_with_AC_from_CSP(Search_problem, Displayable):
    """A search problem with arc consistency and domain splitting

    A node is a CSP """

    def heuristic(self, node):
        sum = 0
        for var in node:
            values = node[var]
            min_cost = 100
            try:
                for x in values:
                    current_cost = self.cons.csp.cost(var, x)
                    if (current_cost < min_cost):
                        min_cost = current_cost
                sum = sum + min_cost
            except:
                sum = 0
        return sum

    def __init__(self, csp):
        self.cons = Con_solver(csp)  # copy of the CSP
        self.domains = self.cons.make_arc_consistent()

    def start_node(self):
        return self.domains

    def is_goal(self, node):
        """node is a goal if all domains have 1 element"""
        return all(len(node[var]) == 1 for var in node)

    def neighbors(self, node):
        """returns the neighboring nodes of node.
        """
        neighs = []
        var = select(x for x in node if len(node[x]) > 1)
        if var:
            dom1, dom2 = partition_domain(node[var])
            self.display(2, "Splitting", var, "into", dom1, "and", dom2)
            to_do = self.cons.new_to_do(var, None)
            for dom in [dom1, dom2]:
                newdoms = copy_with_assign(node, var, dom)
                cons_doms = self.cons.make_arc_consistent(newdoms, to_do)
                if all(len(cons_doms[v]) > 0 for v in cons_doms):
                    # all domains are non-empty
                    neighs.append(Arc(node, cons_doms))
                else:
                    self.display(2, "...", var, "in", dom, "has no solution")
        return neighs


if __name__ == "__main__":

    file_name = ""
    try:
        file_name = sys.argv[1]
    except:
        print("Specify input file!")
        exit()

    domain = {}
    constraints = []
    soft_constraints = []

    # Open the file for reading
    try:
        input_file = open(file_name, "r")
    except:
        print("Error in opening input file!")

    # Convert the text data to an array of strings
    file_data = input_file.readlines()

    # For every line in the array , strip the '\n' character.
    for line in file_data:

        formatted_line = line.strip('\n')

        # If any lines in the input file are
        # comment lines or empty we skip them
        if (formatted_line.startswith('#') or formatted_line.strip() == ''):
            continue;

        split_on_comma = formatted_line.split(', ')
        flag = split_on_comma[0]
        variable = split_on_comma[1]

        if (flag == 'meeting'):

            # Create shallow copy and assign it to each new variable.
            # So in essence each key in the dict gets its own copy of
            # the entire domain.
            domain[variable] = day_time_domain.copy()

        elif (flag == 'domain'):

            # If the flag is 'domain', the constraint can be of 2 types: hard or soft
            # We identify which type it is and depending on the arguments passed we
            # decide which function to pass to the 'Constraint' object constructor
            preference = split_on_comma[2]
            constraint_type = split_on_comma[3]

            if (constraint_type == "soft"):

                # Create a Constraint object using the appropriate
                # 'soft' function comparator. No further parsing required
                soft_constraints.append(Constraint((variable,), s_constraints[preference]()))

            elif (constraint_type == "hard"):

                if (preference in time_list):

                    # If the only argument passed is a 'time' , it uses 'h_time()' as
                    # a functional argument to Constraint constructor
                    constraints.append(Constraint((variable,), h_constriants['time'](preference)))

                elif (preference in days_list):

                    # If the only argument passed is a 'day' , it uses 'h_day()' as
                    # a functional argument to Constraint constructor
                    constraints.append(Constraint((variable,), h_constriants['day'](preference)))

                elif ("-" in preference):

                    # The presence of a '-' character indicates a period of days. We extract the upper and
                    # lower bounds and pass each as a functional parameter to the Constraint constructor
                    date_times = preference.split('-')

                    # extract dt1 and dt2 from text file
                    dt1 = date_times[0]
                    dt2 = date_times[1]

                    # Grab appropriate segment of string representing
                    # day and time for dt1
                    dt1_day  = dt1[0:3]
                    dt1_time = dt1[4:]

                    # Grab appropriate segment of string representing
                    # day and time for dt2
                    dt2_day  = dt2[0:3]
                    dt2_time = dt2[4:]

                    # Package data into tuples to use as outer argument for function
                    dt1_tup = (dt1_day, dt1_time)
                    dt2_tup = (dt2_day, dt2_time)

                    # Add the Constraint object to the list of constraints
                    constraints.append(Constraint((variable,), h_constriants['day-range'](dt1_tup, dt2_tup)))

                else:

                    # Otherwise , the domain constraint is a combination of various factors. We extract data
                    # and match to determine the appropriate 'hard' Constraint function comparator
                    data = preference.split()
                    if (len(data) == 1):

                        # If the argument list is of length 1, the constraints passed must be either
                        # 'morning' or 'afternoon'. Hence, appropriate Constraint objects are made
                        # using the correct function comparator
                        if (data[0] == 'morning'):

                            # (domain , <m> , morning , hard)
                            constraints.append(Constraint((variable,), h_constriants['morning']()))

                        elif (data[0] == 'afternoon'):

                            # (domain , <m> , afternoon , hard)
                            constraints.append(Constraint((variable,), h_constriants['afternoon']()))
                    else:

                        if (data[0] == "before" and len(data) == 2):

                            # (domain , <m> , before <day> , hard)
                            # Convert the data to a tuple before passing to Constriant constructor
                            formatted_data = (data[1],)
                            if (data[1] in days_list):

                                constraints.append(Constraint((variable,), h_constriants['before_day'](formatted_data)))

                            # (domain , <m> , before <time> , hard)
                            elif (data[1] in time_list):

                                # Convert the data to a tuple before passing to Constriant constructor
                                # (Here, the first index does not matter)
                                formatted_data = (data[0], data[1])
                                constraints.append(
                                    Constraint((variable,), h_constriants['before_time'](formatted_data)))

                        elif (data[0] == "after" and len(data) == 2):

                            # (domain , <m> , after <day> , hard)
                            # Convert the data to a tuple before passing to Constriant constructor
                            formatted_data = (data[1],)
                            if (data[1] in days_list):

                                constraints.append(Constraint((variable,), h_constriants['after_day'](formatted_data)))

                            # (domain , <m> , after <time> , hard)
                            elif (data[1] in time_list):

                                # Convert the data to a tuple before passing to Constriant constructor
                                # (Here, the first index does not matter)
                                formatted_data = (data[0], data[1])
                                constraints.append(Constraint((variable,), h_constriants['after_time'](formatted_data)))

                        # (domain , <m> , before <day> <time> , hard)
                        elif (data[0] == "before" and len(data) == 3):

                            formatted_data = (data[1], data[2])
                            constraints.append(
                                Constraint((variable,), h_constriants['before_day_time'](formatted_data)))

                        # (domain , <m> , after <day> <time> , hard)
                        elif (data[0] == "after" and len(data) == 3):

                            formatted_data = (data[1], data[2])
                            constraints.append(Constraint((variable,), h_constriants['after_day_time'](formatted_data)))

        elif (flag == 'constraint'):

            # Splits the constraint line into the following format:
            # ['variable' , 'preference' , 'variable']. This allows
            # us to build a Constraint object which takes a list of
            # tuples and a function pointer
            lst = variable.split(' ')
            constraints.append(Constraint((lst[0], lst[2]), b_constraints[lst[1]]))

    # Creates a CSP problem
    CSP_Node = CostCSP(domain, constraints, soft_constraints)

    # Performs arc consistency and domain splitting on the given problem
    # This search problem is then passed as a parameter to 'AStarModified'
    # which returns a searcher for the problem
    searcher = AStarModified(Search_with_AC_from_CSP(CSP_Node))
    searcher.max_display_level = 0

    try:
        solution = searcher.search().end()
        cost = searcher.problem.heuristic(solution)
        for key, val in solution.items():
            val_list = list(val)
            day = val_list[0][0]
            time = val_list[0][1]
            print(key + ':' + day + ' ' + time)
        print('cost:', cost, sep='')
    except:
        print("No solution")
