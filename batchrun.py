number_of_runs = 5

for x in xrange(0,number_of_runs):
    #execfile("pure_qlearner.py")
    execfile("qlearner_v2.py")
    #execfile("random_walker.py")

print "%s runs completed" % (number_of_runs)


