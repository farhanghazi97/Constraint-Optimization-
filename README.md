# Constraint-Optimization-

With extensive use of AIPython, we construct CSP's to develop optimal solutions to a scheduling problem inspired by the scenario of hosting a number of visitors to an organisation such as a university department.

The cspOptimizer reads in data from an input file, parses it, and uses the data gathered to construct a Constraint Satisfaction Problem (CSP) with domains , variables and constraints. Using the Searcher class available, it then performs arc consistency and domain splitting (using the user-defined heurisitc function) to produce a Searcher that can be used to find an optimal solution to the problem (provided that it exists).

Some basic test cases have been developed (files within 'tests' folder) to see how robust the system performance is. I will update the test suite periodically.
