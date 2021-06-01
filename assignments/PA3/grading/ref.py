import os

with open("test-case.txt", "r") as myfile:
    tests = myfile.read().splitlines()

print(tests)

for test in tests:
    os.system("./lexer " + test + " | ./parser-ref > " + test + ".ref.out 2>&1")
    os.system("./lexer " + test + " | ./parser-PA3 > " + test + ".PA3.out 2>&1")
    os.system("diff " + test + ".ref.out " + test + ".PA3.out > " + test + ".diff")
