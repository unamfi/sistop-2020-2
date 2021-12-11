	.file	"donde_en_la_memoria.c"
	.text
	.globl	cadena1
	.data
	.align 16
	.type	cadena1, @object
	.size	cadena1, 28
cadena1:
	.string	"Yo solo s\303\251 que no s\303\251 nada"
	.comm	cadena_total,8,8
	.globl	tamano
	.align 4
	.type	tamano, @object
	.size	tamano, 4
tamano:
	.long	30
	.section	.rodata
.LC0:
	.string	"Proceso fil\303\263sofo, PID %d\n\n"
.LC1:
	.string	"Yo s\303\263lo s\303\251 que nada s\303\251"
.LC2:
	.string	"Pero si alguien sabe menos"
.LC3:
	.string	"%s\n%s\n%s\n%s\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	tamano(%rip), %eax
	cltq
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -8(%rbp)
	call	getpid@PLT
	movl	%eax, %esi
	leaq	.LC0(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	tamano(%rip), %eax
	movslq	%eax, %rdx
	movq	-16(%rbp), %rax
	leaq	.LC1(%rip), %rsi
	movq	%rax, %rdi
	call	strncpy@PLT
	movl	tamano(%rip), %eax
	movslq	%eax, %rdx
	movq	-8(%rbp), %rax
	leaq	.LC2(%rip), %rsi
	movq	%rax, %rdi
	call	strncpy@PLT
	movl	$0, %eax
	call	construye_final
	movq	%rax, -24(%rbp)
	movl	tamano(%rip), %eax
	sall	$2, %eax
	cltq
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, cadena_total(%rip)
	movl	tamano(%rip), %eax
	sall	$2, %eax
	movslq	%eax, %rsi
	movq	cadena_total(%rip), %rax
	movq	-8(%rbp), %rcx
	movq	-16(%rbp), %rdx
	subq	$8, %rsp
	pushq	-24(%rbp)
	movq	%rcx, %r9
	movq	%rdx, %r8
	leaq	cadena1(%rip), %rcx
	leaq	.LC3(%rip), %rdx
	movq	%rax, %rdi
	movl	$0, %eax
	call	snprintf@PLT
	addq	$16, %rsp
	movq	cadena_total(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movq	stdin(%rip), %rax
	movq	%rax, %rdi
	call	getc@PLT
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	cadena_total(%rip), %rax
	movq	%rax, %rdi
	call	free@PLT
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.section	.rodata
.LC4:
	.string	"puede ser"
	.text
	.globl	construye_final
	.type	construye_final, @function
construye_final:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$80, %rsp
	movabsq	$8246211200043688386, %rax
	movl	$8293, %edx
	movq	%rax, -48(%rbp)
	movq	%rdx, -40(%rbp)
	movl	$0, -32(%rbp)
	movabsq	$9399061139649824, %rax
	movl	$0, %edx
	movq	%rax, -80(%rbp)
	movq	%rdx, -72(%rbp)
	movl	$0, -64(%rbp)
	leaq	.LC4(%rip), %rax
	movq	%rax, -8(%rbp)
	movl	tamano(%rip), %eax
	cltq
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -16(%rbp)
	movl	tamano(%rip), %eax
	movslq	%eax, %rdx
	leaq	-48(%rbp), %rcx
	movq	-16(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	strncat@PLT
	movl	tamano(%rip), %eax
	movslq	%eax, %rdx
	movq	-8(%rbp), %rcx
	movq	-16(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	strncat@PLT
	movl	tamano(%rip), %eax
	movslq	%eax, %rdx
	leaq	-80(%rbp), %rcx
	movq	-16(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	strncat@PLT
	movq	-16(%rbp), %rax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	construye_final, .-construye_final
	.ident	"GCC: (Debian 8.3.0-6) 8.3.0"
	.section	.note.GNU-stack,"",@progbits
