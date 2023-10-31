extrn read_menu_item: near
extrn read_8_signed: near
extrn print_2_signed: near
extrn print_16_unsigned: near

stack SEGMENT PARA STACK 'STACK'
    db 200h DUP(?)
stack ENDS

datas SEGMENT PARA PUBLIC 'DATA'
    menu    db 10, 13, 10, 13, "Choose menu item:", 10, 13
            db "1. Input number (8 signed)", 10, 13
            db "2. Print 2 signed", 10, 13
            db "3. Print 16 unsigned", 10, 13
            db "0. Exit program", 10, 13
            db "Select menu item: $"
    ; тип near 2 байта
    func_arr dw exit_func, read_8_signed, print_2_signed, print_16_unsigned
datas ENDS

codes SEGMENT PARA PUBLIC 'CODE'
    ASSUME    SS: stack, DS: datas

print_menu proc near
    mov ah, 09h
    mov dx, OFFSET menu
    int 21h

    ret
print_menu endp

exit_func proc near
    mov AH, 04Ch
    int 21h
exit_func endp

start:
    mov ax, datas
    mov ds, ax

main:
    call print_menu
    call read_menu_item
    call func_arr[SI]
    jmp  main

codes ENDS

END start