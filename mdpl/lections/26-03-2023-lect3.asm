.186

STK SEGMENT PARA STACK 'STACK'
DB 50h DUP(0)
STK ENDS

DATA SEGMENT PARA PUBLIC 'DATA'
MSG DB "Factorial is:$"
TABL DB "0123456789ABCDEF"
DATA ENDS

CSEG SEGMENT para public 'CODE'
	assume CS:CSEG, DS:DATA
factor:         ; sp = &ip
    push bp     ; sp = &bp(старое)
    mov bp, sp  ; bp = &bp(старое)
	sub sp, 2   ; sp = bp-2
	mov ax, ss:[bp+4]  
	mov ss:[bp-2], ax
	dec ax
	test ax, ax
	jz ret1
	push ax
	call factor
	mov bx, ax
	mov ax, ss:[bp-2]
	mul bx
	jmp exit
	ret1:
	mov ax, 1
	exit:
	add sp, 2
	pop bp
	ret 2
main:
    mov ax, DATA
	mov ds, ax
	
    mov dx, 5
    push dx
	call factor
	
	mov dx, offset MSG
	mov bx, ax
	mov ah, 9
	int 21h
	mov ax, bx

	mov si, ax
	mov bx, offset TABL
	
	mov cx, 4
	cycle:
	rol si, 4
	mov ax, si
	and ax, 15	; 0000 0000 0000 1111
	xlat
	
	mov ah, 2
	mov dl, al
	int 21h
	loop cycle
	
	
	
	mov ax, 4c00h
	int 21h
CSEG ENDS
END main