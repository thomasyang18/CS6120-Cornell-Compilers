	.file	"a.c"
	.text
	.data
	.align 32
	.type	.Lubsan_type0, @object
	.size	.Lubsan_type0, 10
.Lubsan_type0:
	.value	0
	.value	11
	.string	"'int'"
	.zero	54
	.align 32
	.type	.Lubsan_type1, @object
	.size	.Lubsan_type1, 15
.Lubsan_type1:
	.value	0
	.value	7
	.string	"'char [7]'"
	.zero	49
	.section	.rodata
	.align 32
.LC0:
	.string	"a.c"
	.zero	60
	.section	.data.rel.local,"aw"
	.align 32
	.type	.Lubsan_data4, @object
	.size	.Lubsan_data4, 32
.Lubsan_data4:
	.quad	.LC0
	.long	13
	.long	39
	.quad	.Lubsan_type1
	.quad	.Lubsan_type0
	.zero	32
	.data
	.align 32
	.type	.Lubsan_type2, @object
	.size	.Lubsan_type2, 11
.Lubsan_type2:
	.value	-1
	.value	0
	.string	"'char'"
	.zero	53
	.section	.data.rel.local
	.align 32
	.type	.Lubsan_data5, @object
	.size	.Lubsan_data5, 32
.Lubsan_data5:
	.quad	.LC0
	.long	13
	.long	39
	.quad	.Lubsan_type2
	.byte	0
	.byte	0
	.zero	6
	.zero	32
	.align 32
	.type	.Lubsan_data6, @object
	.size	.Lubsan_data6, 16
.Lubsan_data6:
	.quad	.LC0
	.long	13
	.long	39
	.zero	48
	.align 32
	.type	.Lubsan_data7, @object
	.size	.Lubsan_data7, 32
.Lubsan_data7:
	.quad	.LC0
	.long	14
	.long	39
	.quad	.Lubsan_type1
	.quad	.Lubsan_type0
	.zero	32
	.align 32
	.type	.Lubsan_data8, @object
	.size	.Lubsan_data8, 32
.Lubsan_data8:
	.quad	.LC0
	.long	14
	.long	39
	.quad	.Lubsan_type2
	.byte	0
	.byte	0
	.zero	6
	.zero	32
	.align 32
	.type	.Lubsan_data9, @object
	.size	.Lubsan_data9, 16
.Lubsan_data9:
	.quad	.LC0
	.long	14
	.long	39
	.zero	48
	.globl	__asan_stack_malloc_1
	.section	.rodata
.LC1:
	.string	"2 48 4 3 n:6 64 7 6 str:10"
	.align 32
.LC2:
	.string	"%d\n"
	.zero	60
	.align 32
.LC3:
	.string	"%s\n"
	.zero	60
	.section	.data.rel.local
	.align 32
	.type	.Lubsan_data10, @object
	.size	.Lubsan_data10, 24
.Lubsan_data10:
	.quad	.LC0
	.long	13
	.long	33
	.quad	.Lubsan_type0
	.zero	40
	.align 32
	.type	.Lubsan_data11, @object
	.size	.Lubsan_data11, 24
.Lubsan_data11:
	.quad	.LC0
	.long	13
	.long	27
	.quad	.Lubsan_type0
	.zero	40
	.align 32
	.type	.Lubsan_data12, @object
	.size	.Lubsan_data12, 24
.Lubsan_data12:
	.quad	.LC0
	.long	14
	.long	33
	.quad	.Lubsan_type0
	.zero	40
	.align 32
	.type	.Lubsan_data13, @object
	.size	.Lubsan_data13, 24
.Lubsan_data13:
	.quad	.LC0
	.long	14
	.long	27
	.quad	.Lubsan_type0
	.zero	40
	.section	.rodata
	.align 32
.LC4:
	.string	"YES"
	.zero	60
	.align 32
.LC5:
	.string	"NO"
	.zero	61
	.section	.data.rel.local
	.align 32
	.type	.Lubsan_data14, @object
	.size	.Lubsan_data14, 24
.Lubsan_data14:
	.quad	.LC0
	.long	8
	.long	26
	.quad	.Lubsan_type0
	.zero	40
	.text
	.globl	main
	.type	main, @function
main:
.LASANPC0:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$152, %rsp
	.cfi_offset 15, -24
	.cfi_offset 14, -32
	.cfi_offset 13, -40
	.cfi_offset 12, -48
	.cfi_offset 3, -56
	leaq	-176(%rbp), %r12
	movq	%r12, %r15
	cmpl	$0, __asan_option_detect_stack_use_after_return(%rip)
	je	.L1
	movl	$96, %edi
	call	__asan_stack_malloc_1@PLT
	testq	%rax, %rax
	je	.L1
	movq	%rax, %r12
.L1:
	leaq	128(%r12), %rax
	movq	%rax, %rbx
	movq	$1102416563, (%r12)
	leaq	.LC1(%rip), %rax
	movq	%rax, 8(%r12)
	leaq	.LASANPC0(%rip), %rax
	movq	%rax, 16(%r12)
	movq	%r12, %r13
	shrq	$3, %r13
	movl	$-235802127, 2147450880(%r13)
	movl	$-234556943, 2147450884(%r13)
	movl	$-202116345, 2147450888(%r13)
	movq	%fs:40, %rax
	movq	%rax, -56(%rbp)
	xorl	%eax, %eax
	leaq	-80(%rbx), %rax
	movq	%rax, %rsi
	leaq	.LC2(%rip), %rdi
	movl	$0, %eax
	call	__isoc99_scanf@PLT
	movl	$0, -192(%rbp)
	jmp	.L5
.L37:
	movl	$0, -188(%rbp)
	leaq	-64(%rbx), %rax
	shrq	$3, %rax
	addq	$2147450880, %rax
	movb	$7, (%rax)
	leaq	-64(%rbx), %rax
	movq	%rax, %rsi
	leaq	.LC3(%rip), %rdi
	movl	$0, %eax
	call	__isoc99_scanf@PLT
	movl	$0, -184(%rbp)
	jmp	.L6
.L18:
	movl	-184(%rbp), %r14d
	movslq	%r14d, %rax
	cmpq	$6, %rax
	jbe	.L7
	movslq	%r14d, %rax
	movq	%rax, %rsi
	leaq	.Lubsan_data4(%rip), %rdi
	call	__ubsan_handle_out_of_bounds@PLT
.L7:
	leaq	-64(%rbx), %rdx
	movslq	%r14d, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	leaq	-64(%rbx), %rax
	subq	%rax, %rdx
	movq	%rdx, %rax
	leaq	1(%rax), %rdx
	leaq	-64(%rbx), %rcx
	movslq	%r14d, %rax
	addq	%rcx, %rax
	cmpq	$7, %rdx
	jbe	.L8
	movq	%rax, %rcx
	addq	%rcx, %rdx
	cmpq	%rdx, %rcx
	ja	.L8
	movq	%rax, %rsi
	leaq	.Lubsan_data5(%rip), %rdi
	call	__ubsan_handle_type_mismatch_v1@PLT
.L8:
	movslq	%r14d, %rcx
	leaq	-64(%rbx), %rdx
	leaq	(%rdx,%rcx), %rax
	notq	%rcx
	shrq	$63, %rcx
	testb	%cl, %cl
	je	.L10
	cmpq	%rdx, %rax
	jnb	.L11
.L12:
	leaq	-64(%rbx), %rcx
	movq	%rax, %rdx
	movq	%rcx, %rsi
	leaq	.Lubsan_data6(%rip), %rdi
	call	__ubsan_handle_pointer_overflow@PLT
	jmp	.L11
.L10:
	cmpq	%rdx, %rax
	ja	.L12
.L11:
	leaq	-64(%rbx), %rdx
	movslq	%r14d, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	shrq	$3, %rdx
	addq	$2147450880, %rdx
	movzbl	(%rdx), %edx
	testb	%dl, %dl
	setne	%cl
	movq	%rax, %rsi
	andl	$7, %esi
	cmpb	%dl, %sil
	setge	%dl
	andl	%ecx, %edx
	testb	%dl, %dl
	je	.L13
	movq	%rax, %rdi
	call	__asan_report_load1@PLT
.L13:
	movslq	%r14d, %rax
	movzbl	-64(%rbx,%rax), %eax
	movsbl	%al, %eax
	movl	-188(%rbp), %edx
	addl	%eax, %edx
	movl	%edx, %r14d
	jno	.L14
	movslq	%eax, %rdx
	movl	-188(%rbp), %eax
	cltq
	movq	%rax, %rsi
	leaq	.Lubsan_data10(%rip), %rdi
	call	__ubsan_handle_add_overflow@PLT
.L14:
	movl	%r14d, -188(%rbp)
	movl	-184(%rbp), %eax
	addl	$1, %eax
	movl	%eax, %r14d
	jno	.L16
	movl	-184(%rbp), %eax
	cltq
	movl	$1, %edx
	movq	%rax, %rsi
	leaq	.Lubsan_data11(%rip), %rdi
	call	__ubsan_handle_add_overflow@PLT
.L16:
	movl	%r14d, -184(%rbp)
.L6:
	cmpl	$2, -184(%rbp)
	jle	.L18
	movl	$3, -180(%rbp)
	jmp	.L19
.L31:
	movl	-180(%rbp), %r14d
	movslq	%r14d, %rax
	cmpq	$6, %rax
	jbe	.L20
	movslq	%r14d, %rax
	movq	%rax, %rsi
	leaq	.Lubsan_data7(%rip), %rdi
	call	__ubsan_handle_out_of_bounds@PLT
.L20:
	leaq	-64(%rbx), %rdx
	movslq	%r14d, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	leaq	-64(%rbx), %rax
	subq	%rax, %rdx
	movq	%rdx, %rax
	leaq	1(%rax), %rdx
	leaq	-64(%rbx), %rcx
	movslq	%r14d, %rax
	addq	%rcx, %rax
	cmpq	$7, %rdx
	jbe	.L21
	movq	%rax, %rcx
	addq	%rcx, %rdx
	cmpq	%rdx, %rcx
	ja	.L21
	movq	%rax, %rsi
	leaq	.Lubsan_data8(%rip), %rdi
	call	__ubsan_handle_type_mismatch_v1@PLT
.L21:
	movslq	%r14d, %rcx
	leaq	-64(%rbx), %rdx
	leaq	(%rdx,%rcx), %rax
	notq	%rcx
	shrq	$63, %rcx
	testb	%cl, %cl
	je	.L23
	cmpq	%rdx, %rax
	jnb	.L24
.L25:
	leaq	-64(%rbx), %rcx
	movq	%rax, %rdx
	movq	%rcx, %rsi
	leaq	.Lubsan_data9(%rip), %rdi
	call	__ubsan_handle_pointer_overflow@PLT
	jmp	.L24
.L23:
	cmpq	%rdx, %rax
	ja	.L25
.L24:
	leaq	-64(%rbx), %rdx
	movslq	%r14d, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	shrq	$3, %rdx
	addq	$2147450880, %rdx
	movzbl	(%rdx), %edx
	testb	%dl, %dl
	setne	%cl
	movq	%rax, %rsi
	andl	$7, %esi
	cmpb	%dl, %sil
	setge	%dl
	andl	%ecx, %edx
	testb	%dl, %dl
	je	.L26
	movq	%rax, %rdi
	call	__asan_report_load1@PLT
.L26:
	movslq	%r14d, %rax
	movzbl	-64(%rbx,%rax), %eax
	movsbl	%al, %eax
	movl	-188(%rbp), %edx
	subl	%eax, %edx
	movl	%edx, %r14d
	jno	.L27
	movslq	%eax, %rdx
	movl	-188(%rbp), %eax
	cltq
	movq	%rax, %rsi
	leaq	.Lubsan_data12(%rip), %rdi
	call	__ubsan_handle_sub_overflow@PLT
.L27:
	movl	%r14d, -188(%rbp)
	movl	-180(%rbp), %eax
	addl	$1, %eax
	movl	%eax, %r14d
	jno	.L29
	movl	-180(%rbp), %eax
	cltq
	movl	$1, %edx
	movq	%rax, %rsi
	leaq	.Lubsan_data13(%rip), %rdi
	call	__ubsan_handle_add_overflow@PLT
.L29:
	movl	%r14d, -180(%rbp)
.L19:
	cmpl	$5, -180(%rbp)
	jle	.L31
	cmpl	$0, -188(%rbp)
	jne	.L32
	leaq	.LC4(%rip), %rdi
	call	puts@PLT
	jmp	.L33
.L32:
	leaq	.LC5(%rip), %rdi
	call	puts@PLT
.L33:
	leaq	-64(%rbx), %rax
	shrq	$3, %rax
	addq	$2147450880, %rax
	movb	$-8, (%rax)
	movl	-192(%rbp), %eax
	addl	$1, %eax
	movl	%eax, %r14d
	jno	.L34
	movl	-192(%rbp), %eax
	cltq
	movl	$1, %edx
	movq	%rax, %rsi
	leaq	.Lubsan_data14(%rip), %rdi
	call	__ubsan_handle_add_overflow@PLT
.L34:
	movl	%r14d, -192(%rbp)
.L5:
	leaq	-80(%rbx), %rax
	movq	%rax, %rdx
	movq	%rdx, %rax
	shrq	$3, %rax
	addq	$2147450880, %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	setne	%cl
	cmpb	$3, %al
	setle	%al
	andl	%ecx, %eax
	testb	%al, %al
	je	.L36
	movq	%rdx, %rdi
	call	__asan_report_load4@PLT
.L36:
	movl	-80(%rbx), %eax
	cmpl	%eax, -192(%rbp)
	jl	.L37
	movl	$0, %eax
	movl	%eax, %edx
	cmpq	%r12, %r15
	je	.L2
	movq	$1172321806, (%r12)
	movabsq	$-723401728380766731, %rax
	movq	%rax, 2147450880(%r13)
	movl	$-168430091, 2147450888(%r13)
	movq	120(%r12), %rax
	movb	$0, (%rax)
	jmp	.L3
.L2:
	movq	$0, 2147450880(%r13)
	movl	$0, 2147450888(%r13)
.L3:
	movq	-56(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L39
	call	__stack_chk_fail@PLT
.L39:
	movl	%edx, %eax
	addq	$152, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.data.rel.local
	.align 32
	.type	.Lubsan_data0, @object
	.size	.Lubsan_data0, 40
.Lubsan_data0:
	.quad	.LC0
	.long	7
	.long	2
	.quad	0
	.long	0
	.long	0
	.long	1
	.zero	4
	.zero	56
	.align 32
	.type	.Lubsan_data1, @object
	.size	.Lubsan_data1, 40
.Lubsan_data1:
	.quad	.LC0
	.long	11
	.long	3
	.quad	0
	.long	0
	.long	0
	.long	1
	.zero	4
	.zero	56
	.align 32
	.type	.Lubsan_data2, @object
	.size	.Lubsan_data2, 40
.Lubsan_data2:
	.quad	.LC0
	.long	15
	.long	11
	.quad	0
	.long	0
	.long	0
	.long	1
	.zero	4
	.zero	56
	.align 32
	.type	.Lubsan_data3, @object
	.size	.Lubsan_data3, 40
.Lubsan_data3:
	.quad	.LC0
	.long	15
	.long	33
	.quad	0
	.long	0
	.long	0
	.long	1
	.zero	4
	.zero	56
	.section	.rodata
.LC6:
	.string	"*.Lubsan_data14"
.LC7:
	.string	"*.Lubsan_data13"
.LC8:
	.string	"*.Lubsan_data12"
.LC9:
	.string	"*.Lubsan_data11"
.LC10:
	.string	"*.Lubsan_data10"
.LC11:
	.string	"*.Lubsan_data9"
.LC12:
	.string	"*.Lubsan_data8"
.LC13:
	.string	"*.Lubsan_data7"
.LC14:
	.string	"*.Lubsan_data6"
.LC15:
	.string	"*.Lubsan_data5"
.LC16:
	.string	"*.Lubsan_type2"
.LC17:
	.string	"*.Lubsan_data4"
.LC18:
	.string	"*.Lubsan_type1"
.LC19:
	.string	"*.Lubsan_type0"
.LC20:
	.string	"*.Lubsan_data3"
.LC21:
	.string	"*.Lubsan_data2"
.LC22:
	.string	"*.Lubsan_data1"
.LC23:
	.string	"*.Lubsan_data0"
.LC24:
	.string	"*.LC5"
.LC25:
	.string	"*.LC3"
.LC26:
	.string	"*.LC4"
.LC27:
	.string	"*.LC0"
.LC28:
	.string	"*.LC2"
	.section	.data.rel.local
	.align 32
	.type	.LASAN0, @object
	.size	.LASAN0, 1472
.LASAN0:
	.quad	.Lubsan_data14
	.quad	24
	.quad	64
	.quad	.LC6
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data13
	.quad	24
	.quad	64
	.quad	.LC7
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data12
	.quad	24
	.quad	64
	.quad	.LC8
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data11
	.quad	24
	.quad	64
	.quad	.LC9
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data10
	.quad	24
	.quad	64
	.quad	.LC10
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data9
	.quad	16
	.quad	64
	.quad	.LC11
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data8
	.quad	32
	.quad	64
	.quad	.LC12
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data7
	.quad	32
	.quad	64
	.quad	.LC13
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data6
	.quad	16
	.quad	64
	.quad	.LC14
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data5
	.quad	32
	.quad	64
	.quad	.LC15
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_type2
	.quad	11
	.quad	64
	.quad	.LC16
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data4
	.quad	32
	.quad	64
	.quad	.LC17
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_type1
	.quad	15
	.quad	64
	.quad	.LC18
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_type0
	.quad	10
	.quad	64
	.quad	.LC19
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data3
	.quad	40
	.quad	96
	.quad	.LC20
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data2
	.quad	40
	.quad	96
	.quad	.LC21
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data1
	.quad	40
	.quad	96
	.quad	.LC22
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.Lubsan_data0
	.quad	40
	.quad	96
	.quad	.LC23
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.LC5
	.quad	3
	.quad	64
	.quad	.LC24
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.LC3
	.quad	4
	.quad	64
	.quad	.LC25
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.LC4
	.quad	4
	.quad	64
	.quad	.LC26
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.LC0
	.quad	4
	.quad	64
	.quad	.LC27
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.quad	.LC2
	.quad	4
	.quad	64
	.quad	.LC28
	.quad	.LC0
	.quad	0
	.quad	0
	.quad	0
	.text
	.type	_sub_D_00099_0, @function
_sub_D_00099_0:
.LFB1:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$23, %esi
	leaq	.LASAN0(%rip), %rdi
	call	__asan_unregister_globals@PLT
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	_sub_D_00099_0, .-_sub_D_00099_0
	.section	.fini_array.00099,"aw"
	.align 8
	.quad	_sub_D_00099_0
	.text
	.type	_sub_I_00099_1, @function
_sub_I_00099_1:
.LFB2:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	call	__asan_init@PLT
	call	__asan_version_mismatch_check_v8@PLT
	movl	$23, %esi
	leaq	.LASAN0(%rip), %rdi
	call	__asan_register_globals@PLT
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	_sub_I_00099_1, .-_sub_I_00099_1
	.section	.init_array.00099,"aw"
	.align 8
	.quad	_sub_I_00099_1
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
