PUBLIC read_8_signed
PUBLIC read_menu_item

PUBLIC number

extrn print_newline: near
extrn rev_number: near

datas SEGMENT para PUBLIC 'DATA'
    ; само число
    number DW 0
    ; флаг отрицательности числа
    rev_flag db 0
    ; приглашение ввода числа
    invite_num db "Enter number (8 signed): $"
datas ENDS

codes SEGMENT para PUBLIC 'CODE'
    ASSUME ds: datas

read_8_signed proc near
    call print_newline
    call print_newline

    ; выводим приглашение ввода числа
    mov dx, OFFSET invite_num
    mov ah, 09h
    int 21h

    mov rev_flag, 0 ; по умолчанию неотрицательное

    xor dx, dx

    ; 5 потому что в таком случае 
    ; максимально допустимое число в 8 сс это 77777, 
    ; что в переводе  в 10 сс  дает как раз таки 32767 - 
    ; максимальное положительное двухбайтовое число
    mov bx, 5

    mov ah, 01h

    read_digit:

        ; ввели символ (он в al)
        int 21h

        cmp al, '-'
        jne proc_digit

        mov rev_flag, 1
        jmp read_digit

        proc_digit:

            ; отнимаем, чтобы получить правильные коды
            sub al, '0'

            ; цифра в 8 сс кодируется 3 битами
            mov cl, 3
            ; сдвигаем влево на 3 бита,
            ; чтобы добавить очередную прочитанную цифру
            sal dx, cl

            add dl, al

        dec bx
        jnz read_digit

    mov number, dx

    cmp rev_flag, 1
    jne end_read
    
    call rev_number

    end_read:

    ret
read_8_signed endp

read_menu_item proc near
    mov ah, 01h ; считать символ с stdin (в al)
    int 21h
    
    xor ah, ah ; для умножения, чтобы ничего лишнего

    ; отнимаем, чтобы получить правильные коды
    sub al, '0'

    ; элементы массива указателей на функции обработки
    ; имеют тип near (2 байта)
    mov cl, 2
    mul cl
    
    mov si, ax

    ret
read_menu_item endp

codes ENDS

END 