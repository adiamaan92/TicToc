from Queries import populate_user
from Tictoc import Tictoc
from Transaction import Transaction

user_list = populate_user(100, db=False)
T1 = Transaction(user_list)
T2 = Transaction(user_list)
temp_list = populate_user(100, db=False)
algorithm = Tictoc(temp_list)

# Example of serialization
text = 'X = 56\n' \
       'Y = 64\n' \
       'READ1(X)\n' \
       'WRITE2(X)\n' \
       'COMMIT2\n' \
       'WRITE1(Y)\n' \
       'COMMIT1\n'

text2 = 'X = 56\n' \
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

# Example of non-serialization
text4 = 'X = 0\n' \
       'Y = 1\n' \
       'READ1(X)\n' \
       'READ2(X)\n' \
       'WRITE2(X)\n' \
       'WRITE1(X)\n' \
       'COMMIT2\n' \
       'COMMIT1\n'

text4 = text4.splitlines()
algorithm.control_logic(T1, T2, text4)

print("Hey dummy")
