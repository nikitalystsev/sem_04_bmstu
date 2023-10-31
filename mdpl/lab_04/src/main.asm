stacks SEGMENT para STACK 'STACK'
    db 100 DUP(?)
stacks ENDS

datas SEGMENT para public 'DATA'
    n db 1 
    m db 1
    matrix db 9 * 9 DUP(0)
    ind_max_row db 1
    max_sum db 1
    empty_matrix db "Empty matrix$", 10, 13
datas ENDS

public n
public m
public matrix
public ind_max_row
public max_sum
public empty_matrix

extrn input_size: near
extrn input_matrix: near
extrn print_matrix: near
extrn print_newline: near
extrn calc_sum: near
extrn print_sum: near
extrn del_max_row: near
extrn print_size: near
extrn print_index: near
extrn print_empty_mess: near

codes SEGMENT para public 'CODE'
    assume SS:stacks, DS: datas

zero_size:  
    call print_empty_mess
    jmp end_main
    

main:
    mov ax, datas
    mov ds, ax

    call input_size

    cmp n, 0
    je zero_size 

    cmp m, 0
    je zero_size 

    call input_matrix

    call print_newline

    call calc_sum

    call del_max_row

    call print_matrix

    end_main:

    mov ax, 4c00h
	int 21h
    
codes ENDS

END main