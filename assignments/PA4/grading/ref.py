import os

with open("test-cases.txt", "r") as myfile:
    tests = myfile.read().splitlines()

#print(tests)

for test in tests:
    os.system("./lexer " + test + " | ./parser | ./semant-ref > " + test + ".ref.out 2>&1")
    os.system("./lexer " + test + " | ./parser | ./semant-PA4 > " + test + ".PA4.out 2>&1")
    os.system("diff " + test + ".ref.out " + test + ".PA4.out > " + test + ".diff")
