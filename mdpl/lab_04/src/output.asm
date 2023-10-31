public print_newline
public print_space
public print_matrix
public print_sum
public print_size
public print_index
public print_empty_mess

extrn n: byte
extrn m: byte
extrn matrix: byte
extrn ind_max_row: byte
extrn max_sum: byte
extrn empty_matrix: byte

codes SEGMENT para public 'CODE'

print_size proc near
    mov ax, seg n
    mov ds, ax

	mov ah, 2 ; вывод символа в stdout

	mov dl, n 
	int 21h

    call print_space

	mov dl, m 
	int 21h

	ret
print_size endp

print_newline proc near
	mov ah, 2 ; вывод символа в stdout

	mov dl, 10 ; перевод строки
	int 21h
	mov dl, 13 ; возврат каретки
	int 21h

	ret
print_newline endp

print_space proc near
	mov ah, 2
    mov dl, " "
    int 21h

    ret
print_space endp

print_sum proc near
    mov ax, seg n
    mov ds, ax

	mov ah, 2

    mov dl, max_sum
    int 21h

    ret
print_sum endp

print_index proc near
    mov ax, seg n
    mov ds, ax

	mov ah, 2

    mov dl, ind_max_row
    int 21h

    ret
print_index endp

print_empty_mess proc near
    mov ax, seg n
    mov ds, ax

    mov dx, offset empty_matrix
    mov ah, 09h
    int 21h

    ret
print_empty_mess endp

print_matrix proc near
	mov ax, seg n
    mov ds, ax

    cmp n, 0
    jne output_matrix 

    empty_mess:

    mov dx, offset empty_matrix
    mov ah, 09h
    int 21h
    jmp end_print

    output_matrix:

    mov ah, 2 ; вывод символа в stdout

    mov cl, 0

    mov si, 0

    print_row:

        mov dh, 0
        mov bx, 0

        print_digit:

            mov al, matrix[si][bx]
            add al, '0'

            mov dl, al
            int 21h

            call print_space

            inc dh
            inc bx

            cmp dh, m
            jne print_digit

        call print_newline

        add si, 9

        inc cl

        cmp cl, n
        jne print_row

    end_print:

    ret
print_matrix endp

codes ENDS

END