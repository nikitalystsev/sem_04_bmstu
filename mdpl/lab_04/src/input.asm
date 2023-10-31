extrn n: byte
extrn m: byte
extrn matrix: byte

extrn print_newline: near
extrn print_space: near
extrn print_size: near

public input_size
public input_matrix

codes SEGMENT para public 'CODE'

input_size proc near
    mov ax, seg n
    mov ds, ax

    mov ah, 01h
    int 21h
    mov n, al

    ; отнимаем, чтобы получить правильные коды
    sub n, '0'

    call print_space

    mov ah, 01h
    int 21h
    mov m, al

    ; отнимаем, чтобы получить правильные коды
    sub m, '0'

    call print_newline

    ret
input_size endp

input_matrix proc near
    mov ax, seg n
    mov ds, ax

    mov si, 0

    mov cl, 0

    input_row:

        mov bx, 0
        mov dh, 0

        input_digit:
        
            mov ah, 01h
            int 21h

            mov matrix[si][bx], al

            ; отнимаем, чтобы получить правильные коды
            sub matrix[si][bx], '0'

            inc bx
            inc dh

            call print_space

            cmp dh, m
            jne input_digit

        call print_newline
        
        add si, 9

        inc cl
        cmp cl, n
        jne input_row


    ret
input_matrix endp

codes ENDS

END