; описан сегмент стека
STK SEGMENT para STACK 'STACK'
	db 100 dup(0)
STK ENDS

; описан сегмент данных
SD1 SEGMENT para common 'DATA'
	W dw 3444h
SD1 ENDS

; конец модуля
END
