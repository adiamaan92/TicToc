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
scene3 = 'T = 2\n' \
        'X = 0\n' \
        'Y = 1\n' \
        'READ1(X)\n' \
        'READ2(X)\n' \
        'WRITE2(X)\n' \
        'WRITE1(X)\n' \
        'COMMIT2\n' \
        'COMMIT1\n'


# Example of serialization
# the serial schedule is T1T2T3
# the transaction will be successfully completed
scene4 = 'T = 3\n' \
        'X = 32\n' \
        'Y = 76\n' \
        'READ1(X)\n' \
        'WRITE2(X)\n' \
        'WRITE1(X)\n' \
        'COMMIT1\n' \
        'WRITE3(X)\n' \
        'COMMIT2\n' \
        'COMMIT3\n'

# example of non-serialization
# the serial schedule is T2T1T3
# The transaction will be successfully completed
scene5 = 'T = 3\n' \
        'X = 40\n' \
        'Y = 89\n' \
        'READ2(X)\n' \
        'READ1(Y)\n' \
        'WRITE2(X)\n' \
        'COMMIT2\n' \
        'READ3(X)\n' \
        'WRITE1(Y)\n' \
        'COMMIT1\n' \
        'WRITE3(X)\n' \
        'COMMIT3\n'


# Example of Non-serialization transaction
# the T2 Transaction for updating Y will be aborted
scene6 = 'T = 3\n' \
        'X = 12\n' \
        'Y = 10\n' \
        'READ2(X)\n' \
        'READ1(Y)\n' \
        'WRITE2(X)\n' \
        'READ3(X)\n' \
        'WRITE1(Y)\n' \
        'COMMIT1\n' \
        'COMMIT2\n' \
        'WRITE3(X)\n' \
        'COMMIT3\n' \
        'READ2(Y)\n' \
        'WRITE2(Y)\n' \
        'COMMIT2\n'


# This schedule is not conflict-serializable because there is a cycle
# T2 fails when updating X
scene7 = 'T = 3\n' \
        'X = 12\n' \
        'Y = 10\n' \
        'READ2(X)\n' \
        'READ1(Y)\n' \
        'READ3(X)\n' \
        'WRITE1(Y)\n' \
        'COMMIT1\n' \
        'WRITE3(X)\n' \
        'COMMIT3\n' \
        'WRITE2(X)\n' \
        'COMMIT2\n' \
        'READ3(Y)\n' \
        'WRITE3(Y)\n' \
        'COMMIT3\n'

# T2 will be aborted when updating X an Y both
scene8 = 'T = 3\n' \
        'X = 30\n' \
        'Y = 92\n' \
        'READ2(X)\n' \
        'READ1(Y)\n' \
        'WRITE1(Y)\n' \
        'READ3(X)\n' \
        'WRITE3(X)\n' \
        'COMMIT1\n' \
        'COMMIT3\n' \
        'WRITE2(X)\n' \
        'COMMIT2\n' \
        'READ2(Y)\n' \
        'WRITE2(Y)\n' \
        'COMMIT2\n'






