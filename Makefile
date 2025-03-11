a.out: main.cc
	g++ -std=c++17 -O0 -fsanitize=undefined -fsanitize=address \
	-fno-sanitize-recover -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC \
	$^ -o $@

a_fast.out: main.cc
	g++ -std=c++17 -O2 \
	$^ -o $@

.PHONY: in.txt

init:
	touch in.txt out.txt out_expect.txt && \
	cp template.cc main.cc
.PHONY: init

test: a.out in.txt
	./a.out < in.txt > out.txt

ftest: a_fast.out in.txt
	./a_fast.out < in.txt > out.txt

run: a.out
	./a.out

out.txt: test

diff: out.txt out_expect.txt
	diff out.txt out_expect.txt
