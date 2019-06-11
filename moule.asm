extern printf, atoi
section .data
hello : db "Hello world",10,0
nombre: db "%d", 10,0
argc:	dq 0
argv:	dq 0
[DECLS_VARS]


global main
section .text
main :
	push rbp
	mov [argc], rdi
	mov [argv], rsi
	[INIT_VARS]
	[CODE]
	[RETURN]
	pop rbp
	ret
