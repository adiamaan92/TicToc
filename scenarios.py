# A File that will handle all the scenarios

scene = 'T = 2\n' \
       'X = 0\n' \
       'Y = 1\n' \
       'READ1(X)\n' \
       'WRITE2(X)\n' \
       'COMMIT2\n' \
       'WRITE1(Y)\n' \
       'COMMIT1\n'

# Example of serialization - successfull run
scene1 = 'X = 0\n' \
       'Y = 1\n' \
       'READ1(X)\n' \
       'WRITE2(X)\n' \
       'COMMIT2\n' \
       'WRITE1(Y)\n' \
       'COMMIT1\n'

# Runs Successfully
scene2 = 'T = 2\n' \
        'X = 56\n' \
        'Y = 64\n' \
        'READ1(X)\n' \
        'WRITE1(X)\n' \
        'READ2(X)\n' \
        'WRITE2(X)\n' \
        'READ1(Y)\n' \
        'WRITE1(Y)\n' \
        'COMMIT1\n' \
        'READ2(Y)\n' \
        'WRITE2(Y)\n' \
        'COMMIT2\n'

# Example of non-serialization - T1 fails
scene4 = 'T = 2\n' \
        'X = 0\n' \
        'Y = 1\n' \
        'READ1(X)\n' \
        'READ2(X)\n' \
        'WRITE2(X)\n' \
        'WRITE1(X)\n' \
        'COMMIT2\n' \
        'COMMIT1\n'


