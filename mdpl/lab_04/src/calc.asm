extrn n: byte
extrn m: byte
extrn matrix: byte
extrn ind_max_row: byte
extrn max_sum: byte

extrn print_sum: near
extrn print_size: near

public calc_sum
public del_max_row

codes SEGMENT para public 'CODE'
    assume DS: seg n

calc_row_sum proc near
    mov ax, seg n
    mov ds, ax 

    mov al, 0 ; счетчик по столбцам
    mov ah, 0 ; текущая сумма

    mov bx, 0

    column:

        add ah, matrix[si][bx]

        inc bx
        inc al

        cmp al, m
        jne column

    ret
calc_row_sum endp

calc_sum proc near
    mov ax, seg n
    mov ds, ax 

    xor cx, cx

    mov cl, 0

    mov si, 0

    mov max_sum, 0
    mov ind_max_row, cl
    
    row:
        call calc_row_sum

        cmp ah, max_sum
        jle no_update


        update:
            mov max_sum, ah
            mov ind_max_row, cl

        no_update:

        add si, 9

        inc cl

        cmp cl, n
        jne row


    ret
calc_sum endp

del_max_row proc near
    mov ax, seg n
    mov ds, ax 

    xor ax, ax

    mov dh, ind_max_row
    inc dh

    mov al, dh
    mov dh, 9
    mul dh

    mov si, ax

; ################

    xor ax, ax
    xor dx, dx

    mov dh, ind_max_row

    mov al, dh
    mov dh, 9
    mul dh

    mov di, ax

; ################

    xor dx, dx
    mov dl, ind_max_row

    del_row:

        mov bx, 0
        mov ah, 0

        del_column:

            mov al, matrix[si][bx]
            mov matrix[di][bx], al

            inc bx
            inc ah

            cmp ah, m
            jne del_column

        xor cx, cx

        add di, 9
        add si, 9

        inc dl

        cmp dl, n
        jne del_row

    dec n

    ret
del_max_row endp


codes ENDS
END