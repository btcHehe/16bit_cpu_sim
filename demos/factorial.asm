; N! calculation demo (factorial of N)
; INPUT: CX - N
; OUTPUT: AX - N! (result)
start:
    push bx
    push cx
    push dx
    mov ax, 1
    mov cx, 5   ; n in n!
loop:
    mov bx, cx
    dec cx
    jz endfact
    jc endfact  ; if 0!
    jmp mul
endmul:
    jmp loop

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
endfact:
    pop dx
    pop cx
    pop bx
END