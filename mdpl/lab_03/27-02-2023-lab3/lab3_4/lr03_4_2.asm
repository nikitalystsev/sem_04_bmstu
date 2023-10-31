; метка  из другого модуля
EXTRN X: byte

; метку можно использовать в других модулях
PUBLIC exit

; описали сегмент данных 
SD2 SEGMENT para 'DATA'
	Y db 'Y'
SD2 ENDS

; сегмент кода
SC2 SEGMENT para public 'CODE'
	assume CS:SC2, DS:SD2
exit:
	mov ax, seg X
	mov es, ax
	mov bh, es:X

	mov ax, SD2
	mov ds, ax

	xchg ah, Y
; прямая адресация
	xchg ah, ES:X
	xchg ah, Y	

	mov ah, 2 ; вывод на stdout
	mov dl, Y
	int 21h	
	
	mov ax, 4c00h
	int 21h
SC2 ENDS
END