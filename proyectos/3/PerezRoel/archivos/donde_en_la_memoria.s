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
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp         
	.cfi_def_cfa_register 6
	subq	$32, %rsp           #stack frame de 32 bytes para las variables locales, desde rbp
	movl	tamano(%rip),$eax   #guarda el tamaño (global) en eax
	cltq                        #eax(32) -> rax(64) 
	movq	%rax, %rdi          #rax -> rdi
	call	malloc@PLT          #llamada a malloc, toma rdi (tamaño) de parámetro, devuelve dirección en rax
	movq	%rax, -24(%rbp)     #guarda la direccion en el stack rbp-24 (cadena3) 
	call	getpid@PLT          #llamada al getpid, devuelve direccion en eax
	movl	%eax, %esi          #eax -> esi
	leaq	.LC0(%rip), %rdi    #dir.'Proceso filosofo...'->rdi
	movl	$0, %eax            #0 -> eax
	call	printf@PLT          #llamada a printf, toma eax, rdi y esi como parámetros. 
	movl	tamano(%rip), %eax  #dir.tamano(30) -> eax 
	movslq	%eax, %rdx          #eax -> rdx
	movq	-16(%rbp), %rax     #rbp-16(cadena2) -> rax
	leaq	.LC1(%rip), %rsi    #dir."Yo solo se que no se nada" -> rsi
	movq	%rax, %rdi          #rax -> rdi
	call	strncpy@PLT         #llamada a strncpy (toma de parametro rsi,rdi,rdx)
	movl	tamano(%rip), %eax  #tamaño(30) -> eax
	movslq	%eax, %rdx          #eax -> rdx
	movq	-24(%rbp), %rax     #rbp-24(cadena3) -> rax
	leaq	.LC2(%rip), %rsi    #dir.('Pero si alguien...') -> rsi
	movq	%rax, %rdi          #rax->rdi
	call	strncpy@PLT         #llamada a strncpy(toma de parametro rsi,rdi,rdx)
	movl	$0, %eax            #0 -> eax
	call	construye_final     #llamada a construye_final
	movq	%rax, -8(%rbp)      #resultado de construye_final -> rbp-8 (cadena4)
	movl	tamano(%rip), %eax  #tamano -> eax
	sall	$2, %eax            #shift 2 a la izquierda (multiplicar por 4)
	cltq                        #eax -> rax
	movq	%rax, %rdi          #rax -> rdi
	call	malloc@PLT          #llamada a malloc, toma rdi como parametro
	movq	%rax, cadena_total(%rip)    #la direccion se guarda en cadena_total*
	movl	tamano(%rip), %eax  #tamano(30) -> eax
	sall	$2, %eax            #se multiplica por 4 
	movslq	%eax, %rsi          #eax -> rsi
	movq	cadena_total(%rip), %rax    #dir.cadena_total -> rax
	movq	-24(%rbp), %rcx     #cadena3 -> rcx
	movq	-16(%rbp), %rdx     #cadena2 -> rdx
	subq	$8, %rsp            #se resta 8 a rsp (???)
	pushq	-8(%rbp)            #push cadena4 (parametro?)
	movq	%rcx, %r9           #rcx -> r9 cadena3 
	movq	%rdx, %r8           #rdx -> r8 cadena2
	leaq	cadena1(%rip), %rcx #cadena1 -> rcx
	leaq	.LC3(%rip), %rdx    #dir.'%s\n%s\n%s\n%s\n' -> rdx
	movq	%rax, %rdi          #rax -> rdi 
	movl	$0, %eax            #0->eax
	call	snprintf@PLT        #llamada a snprintf. Parámetros: r8,r9,eax,rdi,cadena4
	addq	$16, %rsp           #se suma 16 a rsp
	movq	cadena_total(%rip), %rax    #apuntador a cadena_total -> rax
	movq	%rax, %rdi          #rax -> rdi
	call	puts@PLT            #llamada a puts, toma a la cadena_total como parametro
	movq	stdin(%rip), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	-8(%rbp), %rax
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
.LFE5:
	.size	main, .-main
	.section	.rodata
.LC4:
	.string	"puede ser"
	.text
	.globl	construye_final
	.type	construye_final, @function
construye_final:
.LFB6:
	.cfi_startproc
	pushq	%rbp                        #empuja rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp                  #rsp -> rbp
	.cfi_def_cfa_register 6
	subq	$80, %rsp                   #stack frame de 80 bytes
	movq	%fs:40, %rax                #sentinela (?)
	movq	%rax, -8(%rbp)              #
	xorl	%eax, %eax                  #cosas de cifrado
	movabsq	$8246211200043688386, %rax  #'!siempr' -> rax
	movl	$8293, %edx                 #'e ' -> edx
	movq	%rax, -64(%rbp)             #rax -> rbp-64 (parte1 (64-32))
	movq	%rdx, -56(%rbp)             #rax -> rbp-56 (parte1)
	movl	$0, -48(%rbp)               #0-> rbp-48 (lo que sobra de parte1)
	movabsq	$9399061139649824, %rax     #' usted!' -> rax
	movl	$0, %edx                    #0 -> edx
	movq	%rax, -32(%rbp)             #rax -> rbp-32 (parte3 (32-0))
	movq	%rdx, -24(%rbp)             #rdx -> rbp-24 (parte3)
	movl	$0, -16(%rbp)               #0 -> rbp-16 (parte3) 
	leaq	.LC4(%rip), %rax            #dir.'puede ser' -> rax 
	movq	%rax, -80(%rbp)             #rax -> rbp-80 (parte2)
	movl	tamano(%rip), %eax          #tamano(30) -> eax
	cltq                                #eax -> rax
	movq	%rax, %rdi                  #rax -> rdi
	call	malloc@PLT                  #llamada a malloc, toma a rdi de parámetro
	movq	%rax, -72(%rbp)             #almacena la direccion en rbp-72 (completa)
	movl	tamano(%rip), %eax          #tamano(30) -> eax
	movslq	%eax, %rdx                  #eax -> rdx
	leaq	-64(%rbp), %rcx             #parte1 -> rcx
	movq	-72(%rbp), %rax             #completa -> rax
	movq	%rcx, %rsi                  #rcx -> rsi (source)
	movq	%rax, %rdi                  #rax -> rdi (destination)
	call	strncat@PLT                 #llamada a strncat. Agrega parte1 a completa.
	movl	tamano(%rip), %eax          #tamano -> eax
	movslq	%eax, %rdx                  #eax -> rdx
	movq	-80(%rbp), %rcx             #parte2 -> rcx
	movq	-72(%rbp), %rax             #completa -> rax
	movq	%rcx, %rsi                  #rcx -> rsi (source)
	movq	%rax, %rdi                  #rax -> rdi (destination)
	call	strncat@PLT                 #strncat. Se agrega parte2 a completa
	movl	tamano(%rip), %eax          #tamano -> eax
	movslq	%eax, %rdx                  #eax -> rdx
	leaq	-32(%rbp), %rcx             #parte3 -> rcx
	movq	-72(%rbp), %rax             #completa -> rax
	movq	%rcx, %rsi                  #rcx -> rsi (source)
	movq	%rax, %rdi                  #rax -> rdi (destination)
	call	strncat@PLT                 #strncat. Se agrega parte3 a completa
	movq	-72(%rbp), %rax             #completa -> rax (se retorna completa*)
	movq	-8(%rbp), %rsi              
	xorq	%fs:40, %rsi                #cosas de seguridad del stack
	je	.L5
	call	__stack_chk_fail@PLT
.L5:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	construye_final, .-construye_final
	.ident	"GCC: (Ubuntu 7.3.0-16ubuntu3) 7.3.0"
	.section	.note.GNU-stack,"",@progbits
