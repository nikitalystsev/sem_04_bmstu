;описал сегмент стека
StkSeg SEGMENT PARA STACK 'STACK'
	DB 200h DUP (?)
StkSeg ENDS

; описал сегмент данных
DataS SEGMENT WORD 'DATA'
HelloMessage DB 13               ;курсор поместить в нач. строки
			 DB 10               ;перевести курсор на нов. строку
			 DB 'Hello, world !' ;текст сообщения
			 DB '$'              ;ограничитель для функции DOS
DataS ENDS

;описал сегмент кода
Code SEGMENT WORD 'CODE'
	ASSUME DS:DataS, CS:Code
	
Displ_mess:		
	mov AX, DataS
	mov DS, AX
	mov DX, OFFSET HelloMessage
	mov CX, 3

	count:			
		mov AH, 9
		int 21h
		loop count

	mov AH,4Ch
	int 21h

Code ENDS

END Displ_mess