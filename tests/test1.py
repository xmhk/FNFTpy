from testfunctions import kdvvexample, \
    nsepexample, nsevexample

TO = nsepexample(verbose=False)
TO = kdvvexample(verbose=False)
TO = nsevexample(verbose=False)
print(TO.res)