; метку можно использовать в другом модуле
PUBLIC X

; метка в другом сегменте
EXTRN exit: far

; сегмент стека
SSTK SEGMENT para STACK 'STACK'
	db 100 dup(0)
SSTK ENDS

; сегмент данных
SD1 SEGMENT para public 'DATA'
	X db 'X'
SD1 ENDS

; сегмент кода
SC1 SEGMENT para public 'CODE'
	assume CS:SC1, DS:SD1
main:	
	jmp exit
SC1 ENDS
END main