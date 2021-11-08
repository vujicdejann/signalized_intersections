Algorithm Developer Intern Task

Signalized intersections are one of the most prevalent bottleneck types in urban environments, and thus traffic signal control plays a vital role in urban traffic management. There are many different ways to optimize traffic flow from naive and elementary approaches to complex machine learning driven algorithms. Your task will be to optimize the single phase of a traffic signal.
A traffic phase is defined as the green, change, and clearance intervals (the last two we ignore in this task) in a cycle assigned to specified movement(s) of traffic. A cycle is defined as the total time to complete one sequence of signalization for all movements at an intersection.

For a given cycle length C (in seconds) we calculate the array A of length k*C where A[i] represents the number of cars arriving at the second i at a particular phase and k is the number of cycles that we are looking to optimize. We assume that if the phase was active (signal is green) at a given second all the cars arriving at that second will go through the intercession (this is not always realistic).

The objective of the task is to optimize the number of cars arriving at green at a single phase of an intersection. As you probably know, this is not a trivial task because there are many constraints that a traffic light must obey (for example you can not leave just one phase active and never change it, or on the other extreme you can not change the phase every second). 

In our simplified scenario, given the cycle length C we have the following constraints:
Minimal amount of green time in seconds g_min (you can not change the phase for at least g_min seconds)
Maximal amount of green time in seconds g_max (you must change the phase after g_max seconds)
Minimal amount of red time in seconds r_min (after changing the phase you have to wait at least r_min seconds to change back to it)
If a cycle ends with green, the next cycle can not start with green.

So, for a given input (see the attached file here) C, k, A, g_min, g_max, r_min your task is to return the array (write it to a file solution.out) P of length k*C where P[i] = 0 or P[i] = 1 (0 represents red and 1 represents green) which maximizes the sum i=1k*CP[i]*A[i], and the array P satisfies all the constraints given above.

For example if

k=2
C=10
A = [0,0,3,4,3,3,3,0,2,1,0,0,0,0,0,3,4,3,0,0]
g_min = 3
g_max = 7
r_min = 2
One solution is
P = [0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0].

One way to get a solution is to brute force all the possible arrays P or to use dynamic programming, but we are looking for a more innovative approach (keep in mind that C is usually in the range of  90-180 and k around 900). Solutions using heuristic methods (e.g. genetic algorithms, simulated annealing, etc.) are preferred.

Although we would prefer the solution in Python you are free to submit your solution in any language. Please send us clean and well commented code. In addition you can submit a presentation (up to 5 slides long) describing your solution in more detail.

Internship task - Miovision




