from Queries import populate_user
from Tictoc import Tictoc
from Transaction import Transaction

user_list = populate_user(100, db=False)
T1 = Transaction(user_list)
example_user = T1.read_element(check_id=4)
T1.write_element(check_id=4, change="Dummy")
algorithm = Tictoc(user_list)
text = 'X = 56\n' \
       'Y = 64\n' \
       'READ1(X)\n ' \
       'SLEEP1'

text = text.splitlines()
algorithm.algo_parser(text=text)

print("Hey dummy")
