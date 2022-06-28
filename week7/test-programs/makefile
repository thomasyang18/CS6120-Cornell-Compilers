CC = clang
CFLAGS = -Xclang -load -Xclang ../build/skeleton/libSkeletonPass.* -Wall -Werror -std=c99

%: %.o
	$(CC) $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
