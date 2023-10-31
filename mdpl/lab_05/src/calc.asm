PUBLIC rev_number

extrn number: word

codes SEGMENT PARA PUBLIC 'CODE'

rev_number proc near
    neg number
    ret
rev_number endp

codes ENDS
END