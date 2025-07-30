a.out: main.cc
	g++ -std=c++17 -O0 -fsanitize=undefined -fsanitize=address \
	-fno-sanitize-recover -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC \
	$^ -o $@

a_fast.out: main.cc
	g++ -std=c++17 -O2 \
	$^ -o $@

a_debug.out: main.cc
	g++ -std=c++17 -g -O0 $^ -o $@

.PHONY: in.txt

init:
	> in.txt & \
	> out.txt & \
	> out_expect.txt & \
	cp template.cc main.cc
.PHONY: init

test: a.out in.txt
	./a.out < in.txt > out.txt

ftest: a_fast.out in.txt
	./a_fast.out < in.txt > out.txt

run: a.out
	./a.out

memcheck: a_debug.out in.txt
	valgrind --leak-check=full ./a_debug.out < in.txt

out.txt: test

diff: out.txt out_expect.txt
	if diff -Bb out.txt out_expect.txt; then echo "\e[1;32mOK\e[0m"; fi
