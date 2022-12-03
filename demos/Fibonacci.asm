; Calculating n-th number from Fibonacci sequence
; INPUT: CX - N
; OUTPUT: AX - N-th Fibonacci number
startfib:
	push bx
	push cx
	mov ax, 0   ; ax - Fn-1
	mov bx, 1   ; bx - Fn-2
	mov cx, 10	; n-th Fibonacci number to find
loop:
    push ax     ; Fn-1 -> Fn-2
    add ax, bx  ; ax - Fn-1 + Fn-2
    pop bx      ; bx - Fn-2
    dec cx      ; one less iteration to do
   	jz endfib   ; if cx == 0 end
	jmp loop    ; else continue
endfib:         ; Fn in ax
	pop bx
	pop cx
END