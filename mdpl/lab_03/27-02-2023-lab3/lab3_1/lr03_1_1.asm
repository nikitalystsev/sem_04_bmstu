; прога отрабатывает и завершает работу, ничего не выводит
; описывает метку, определенную в другом модуле
; near - адрес в том же сегменте
EXTRN output_X: near

; описан сегмент стека
STK SEGMENT PARA STACK 'STACK'
	db 100 dup(0)
STK ENDS


; описан сегмент данных
DSEG SEGMENT PARA PUBLIC 'DATA'
	X db 'R'
DSEG ENDS

; описан сегмент кода
CSEG SEGMENT PARA PUBLIC 'CODE'
	assume CS:CSEG, DS:DSEG, SS:STK
main:
	mov ax, DSEG
	mov ds, ax

; Сохраняет текущий адрес в стеке 
; и передает управление по адресу, 
; указанному в операнде.
	call output_X	

	mov ax, 4c00h
	int 21h
CSEG ENDS

; Метка, объявленная директивой PUBLIC, 
; становится доступной для других модулей программы. 
PUBLIC X

; конец модуля с точкой входа
END main