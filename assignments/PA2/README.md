README file for Programming Assignment 2 (C++ edition)
=====================================================

Your directory should contain the following files:

 Makefile
 README
 cool.flex
 test.cl
 lextest.cc      -> [cool root]/src/PA2/lextest.cc
 mycoolc         -> [cool root]/PA2/mycoolc
 stringtab.cc    -> [cool root]/PA2/stringtab.cc
 utilities.cc    -> [cool root]/PA2/utilities.cc
 handle_flags.cc -> [cool root]/PA2/handle_flags.cc
 *.d             dependency files
 *.*             other generated files

The include (.h) files for this assignment can be found in
[cool root]/PA2

	The Makefile contains targets for compiling and running your
	program. DO NOT MODIFY.

	The README contains this info. Part of the assignment is to fill
	the README with the write-up for your project. You should
	explain design decisions, explain why your code is correct, and
	why your test cases are adequate. It is part of the assignment
	to clearly and concisely explain things in text as well as to
	comment your code. Just edit this file.

	cool.flex is a skeleton file for the specification of the
	lexical analyzer. You should complete it with your regular
	expressions, patterns and actions.

	test.cl is a COOL program that you can test the lexical
	analyzer on. It contains some errors, so it won't compile with
	coolc. However, test.cl does not exercise all lexical
	constructs of COOL and part of your assignment is to rewrite
	test.cl with a complete set of tests for your lexical analyzer.

	cool-parse.h contains definitions that are used by almost all parts
	of the compiler. DO NOT MODIFY.

	stringtab.{cc|h} and stringtab_functions.h contains functions
        to manipulate the string tables.  DO NOT MODIFY.

	utilities.{cc|h} contains functions used by the main() part of
	the lextest program. You may want to use the strdup() function
	defined in here. Remember that you should not print anything
	from inside cool.flex! DO NOT MODIFY.

	lextest.cc contains the main function which will call your
	lexer and print out the tokens that it returns.  DO NOT MODIFY.

	mycoolc is a shell script that glues together the phases of the
	compiler using Unix pipes instead of statically linking code.
	While inefficient, this architecture makes it easy to mix and match
	the components you write with those of the course compiler.
	DO NOT MODIFY.

        cool-lexer.cc is the scanner generated by flex from cool.flex.
        DO NOT MODIFY IT, as your changes will be overritten the next
        time you run flex.

 	The *.d files are automatically generated Makefiles that capture
 	dependencies between source and header files in this directory.
 	These files are updated automatically by Makefile; see the gmake
 	documentation for a detailed explanation.

Instructions
------------

To compile your lextest program type:

% make lexer

Run your lexer by putting your test input in a file 'foo.cl' and
run the lextest program:

% ./lexer foo.cl

To run your lexer on the file test.cl type:

% make dotest

If you think your lexical analyzer is correct and behaves like
the one we wrote, you can actually try 'mycoolc' and see whether
it runs and produces correct code for any examples.
If your lexical analyzer behaves in an
unexpected manner, you may get errors anywhere, i.e. during
parsing, during semantic analysis, during code generation or
only when you run the produced code on spim. So beware.

If you change architectures you must issue

% make clean

when you switch from one type of machine to the other.
If at some point you get weird errors from the linker,
you probably forgot this step.

GOOD LUCK!

---8<------8<------8<------8<---cut here---8<------8<------8<------8<---

Write-up for PA2
----------------

A.1 Compile with flex
    flex -d -ocool-lex.cc cool.flex

 dependencies
    /bin/sh -ec 'g++ -MM -I. -I../../include/PA2 -I../../src/PA2 cool-lex.cc | sed '\''s/\(cool-lex\.o\)[ :]*/\1 cool-lex.d : /g'\'' > cool-lex.d'

B.1 Compile lexttest.cc -> lextest.o
    g++ -g -Wall -Wno-unused -Wno-write-strings -I. -I../../include/PA2 -I../../src/PA2 -c lextest.cc

B.2 Compile utilities.cc -> utilities.o
    g++ -g -Wall -Wno-unused -Wno-write-strings -I. -I../../include/PA2 -I../../src/PA2 -c utilities.cc

OBS => WARNING
utilities.cc: In function 'char* strdup(const char*)':
utilities.cc:220:3: warning: nonnull argument 's' compared to NULL [-Wnonnull-compare]
   if (s == NULL) return(NULL);
   ^~

B.3 Compile stringtab.cc -> stringtab.o
    g++ -g -Wall -Wno-unused -Wno-write-strings -I. -I../../include/PA2 -I../../src/PA2 -c stringtab.cc

B.4 Compile handle_flags.cc -> handle_flags.o
    g++ -g -Wall -Wno-unused -Wno-write-strings -I. -I../../include/PA2 -I../../src/PA2 -c handle_flags.cc

B.5 Compile cool-lex.cc -> cool-lex.o
    g++ -g -Wall -Wno-unused -Wno-write-strings -I. -I../../include/PA2 -I../../src/PA2 -c cool-lex.cc

C.1 Link it all together to build standalone lexer for testing
    g++ -g -Wall -Wno-unused -Wno-write-strings -I. -I../../include/PA2 -I../../src/PA2 \
        lextest.o utilities.o stringtab.o handle_flags.o cool-lex.o \
        -lfl \
        -o lexer

-lfl => ERROR!!!!!
/usr/lib/gcc/i686-linux-gnu/7/../../../../lib/libfl.so: undefined reference to `yylex'
collect2: error: ld returned 1 exit status
Makefile:39: recipe for target 'lexer' failed
make: *** [lexer] Error 1

If the linker can't find its libraries, there's probably something wrong in your setup or
you perhaps have libfl, not libl, and whatever Makefile you're using doesn't know that.

And by the way, the code in libfl is soooo trivial - you might consider not linking with libfl at all in your code.

IIRC, libfl is only there for POSIX compatibility [1](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/lex.html)
and any package should provide replacements instead of depending on it. (`%option noyywrap` or even a simple `-D'yywrap()=((int)1)'`
would work in place of `-lfl` most of the time.)

=====

I'm using arch linux on 2016-12-08, and had difficulties using libfl.so - it couldn't link the yylex symbol correctly.
The solution was to set the line `%option noyywrap` in the `cool.flex` file and remove the `-lfl` part of the LIB= line
in the makefile.

The flex library (libfl.so) references the yylex function but does not define it, and (I think) because we are using C++,
the function name gets mangled before we link to libfl.so. In any case, we don't need the library, as it is mainly concerned
with multiple .flex input files, so with the option above we can safely not link against it.

A more complete solution would declare & define yylex as extern "C" in order to not C++ mangle the name of it in the symbol
table of our object code so it provides what libfl.so expects.

====

Test that the following works

```bash
$ make lexer
```
...

```bash
$ cp /usr/class/cs143/examples/hello_world.cl .
$ ./mycoolc hello_world.cl
$ spim hello_world.s
SPIM Version 6.5 of January 4, 2003
Copyright 1990-2003 by James R. Larus (larus@cs.wisc.edu).
All Rights Reserved.
See the file README for a full copyright notice.
Loaded: /usr/class/cs143/lib/trap.handler
Hello, World.
COOL program successfully executed
Stats -- #instructions : 154
#reads : 27 #writes 22 #branches 28 #other 77
```

====

How to Submit

1. Download the grading script from here and put it in the directory in which you are doing the assignment (where the cool.flex or cool.lex file is). The easiest way to do so is to go to your assignment directory, and run in the VMls:

```
wget http://spark-university.s3.amazonaws.com/stanford-compilers/scripts/pa1-grading.pl
```

This will save the script (pa1-grading.pl) in your assignment directory.

2. Run the script by typing (Note that you can also make the script executable by running `chmod a+x pa1-grading.pl` first, and then running it directly as `./pa1-grading.pl`
)

```
perl pa1-grading.pl
```

3. The script will give you a grade at the end, as well as a submission code. If you want to figure out why your lexer is failing certain tests, the tests will be put in the ./grading subdirectory. The output from your code will be in the ./grading/test-output directory.

4. Once you are satisfied with your grade, click on the arrow above or beneath to go to the "Programming Assignment 1 Submission" quiz. You can use this link to go directly to the quiz. Copy-and-paste the code from the script (to copy from the terminal in VirtualBox, use ctrl+shift+c) into the "Submission code:" box. Once you submit the quiz, your score should appear for the quiz. You can also resubmit the quiz if you wish to update your grade.

