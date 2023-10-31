PUBLIC print_2_signed
PUBLIC print_16_unsigned
PUBLIC print_newline

extrn number: word

extrn rev_number: near

datas SEGMENT PARA PUBLIC 'DATA'
    out_buffer  DB 18 DUP('$')
    mask16      DW 0F000h
    mask8       DW 07000h
    mask2       DW 08000h
datas ENDS

codes SEGMENT para PUBLIC 'CODE'
    assume ds: datas

print_newline proc near
	mov ah, 2 ; вывод символа в stdout

	mov dl, 10 ; перевод строки
	int 21h
	mov dl, 13 ; возврат каретки
	int 21h

	ret
print_newline endp

print_16_unsigned proc near
    call print_newline
    call print_newline

    xor si, si
    xor cx, cx

    mov dx, 4

    mov bx, number

    get_digit16u:

        mov ax, mask16
        and ax, bx ; старшая часть числа (первая цифра)
        mov cl, 4
        shl bx, cl ; обработать следующую цифру

        mov cl, 4
        shr ah, cl ; так извлекаем первую цифру
        add ah, '0' ; получаем символ, соотв. аски коду

        cmp ah, ':'
        jl write_digit16

        add ah, 7 ; число переводим в цифру (шестнадцатиричную)

        write_digit16:
            mov out_buffer[si], ah
            inc si

        dec dx
        jnz get_digit16u

    mov out_buffer[si], '$'
    
    mov ah, 09h
    mov dx, OFFSET out_buffer
    int 21h

    ret
print_16_unsigned endp

print_2_signed proc near
    call print_newline
    call print_newline
    
    xor si, si
    xor cx, cx

    mov dx, 16
    mov bx, number

    test bx, mask2
    jz get_digit2s

    mov dl, '-'
    mov ah, 02h
    int 21h

    dec bx
    not bx
    mov dx, 16

    get_digit2s:
        mov ax, mask2
        and ax, bx ; старшая цифра
        shl bx, 1 ; обработать следующую цифру

        mov cl, 7
        shr ah, cl ; извлекаем первую цифру
        add ah, '0' ; получаем символ, соотв. аски коду
        mov out_buffer[si], ah
        inc si

        dec dx
        jnz get_digit2s

    mov out_buffer[si], '$'
    mov ah, 09h
    mov dx, OFFSET out_buffer
    int 21h

    ret
print_2_signed endp

codes ENDS

END