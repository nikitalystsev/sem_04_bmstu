; модуль вывода и вычисления разности 2-й и 3-й цифры 

; определяю метки как публичные, то есть такие, 
; что их можно использовать в другом модуле
PUBLIC inputstring
PUBLIC calc_diff

; описываю сегмент данных 
datas SEGMENT WORD PUBLIC 'DATA'
	inputstring DB 7 DUP (?)
datas ENDS

;описал сегмент кода
codes SEGMENT PARA  'CODE'
	assume cs:codes, ds:datas

calc_diff:
	mov ax, datas
	mov ds, ax

	; символ перевода строки
	mov dl, 0Ah
	mov ah, 06h
	int 21h

	; загружаю в индексный регистр si адрес (смещение) inputstring
	mov si, OFFSET inputstring
	; загружаю значение 2-й цифры в СL
	mov cl, [si + 1]
	; загружаю значение 3-й цифры в BL
	mov bl, [si + 2]

	; вычисляю разность 2-й и 3-й цифр (результат в cl)
	; если отрицательно, то флаг ZF = 1
	sub cl, bl

	; условие: если нет знака, то есть положительно (флаг ZF=0), 
	; то переход к метке positive
	jns positive

	; смена знака на противоположный
	neg cl

	; выводим знак минус
	mov dl, '-'
	mov ah, 02h
	int 21h

	; вывод цифры
	positive:
		; прибавление кода символа '0' (код ASCII 30h) к числу, 
		; которое мы хотим преобразовать в символ, 
		; позволяет нам получить код символа, 
		; который соответствует этому числу в таблице ASCII.
		add cl, '0'

		; выводим саму цифру
		mov dl, cl
		mov ah, 02h
		int 21h

	;АН=4Ch завершить процесс
	mov AH, 4Ch 
	int 21h 

codes ENDS

END 