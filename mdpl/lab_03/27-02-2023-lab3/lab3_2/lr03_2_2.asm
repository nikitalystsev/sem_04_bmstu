; прога на линуксе выводит символы D4

; описан сегмент данных (накладываются друг на друга)
SD1 SEGMENT para common 'DATA'
; label определяет метку и задает ее тип
; Метка получает значение, равное адресу следующей команды 
; или следующих данных, и тип,
; указанный явно
	C1 LABEL byte
; устанавливает значение программного счетчика
	ORG 1h
	C2 LABEL byte
SD1 ENDS

; описан сегмент кода
CSEG SEGMENT para 'CODE'
	ASSUME CS:CSEG, DS:SD1
main:
	mov ax, SD1
	mov ds, ax

	mov ah, 2 ; вывести символ в stdout
	
	mov dl, C1 
	int 21h

	mov dl, C2 
	int 21h

	mov ax, 4c00h
	int 21h
CSEG ENDS
END main