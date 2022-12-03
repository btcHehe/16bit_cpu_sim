; N! calculation demo (factorial of N)
; INPUT: CX - N
; OUTPUT: AX - N! (result)
start:
    push bx
    push cx
    push dx
    mov ax, 1
    mov cx, 5   ; n in n!
petla:
    mov bx, cx
    dec cx
    jz endsilnia
    jc endsilnia    ; if 0!
    jmp mul
endmul:
    jmp petla

; ax, bx - parameters 
; ax - result
mul:
    mov dx, ax
    dec bx
mulloop:
    add ax, dx
    dec bx
    jz endmul
    jmp mulloop
endsilnia:
    pop dx
    pop cx
    pop bx
END