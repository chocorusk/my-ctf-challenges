BITS 64
global check

check:
	xor	eax, eax

	cmp	byte [rdi+0], 0x41
	jne	.ret
	cmp	byte [rdi+35], 0x7d
	jne	.ret
	cmp	byte [rdi+1], 0x6c
	jne	.ret
	cmp	byte [rdi+16], 0x6e
	jne	.ret
	cmp	byte [rdi+4], 0x63
	jne	.ret
	cmp	byte [rdi+20], 0x39
	jne	.ret
	cmp	byte [rdi+5], 0x61
	jne	.ret
	cmp	byte [rdi+8], 0x61
	jne	.ret
	cmp	byte [rdi+23], 0x61
	jne	.ret
	cmp	byte [rdi+18], 0x34
	jne	.ret
	cmp	byte [rdi+26], 0x6e
	jne	.ret
	cmp	byte [rdi+9], 0x77
	jne	.ret
	cmp	byte [rdi+12], 0x69
	jne	.ret
	cmp	byte [rdi+10], 0x34
	jne	.ret
	cmp	byte [rdi+13], 0x5f
	jne	.ret
	cmp	byte [rdi+15], 0x69
	jne	.ret
	cmp	byte [rdi+30], 0x70
	jne	.ret
	cmp	byte [rdi+14], 0x6d
	jne	.ret
	cmp	byte [rdi+32], 0x63
	jne	.ret
	cmp	byte [rdi+33], 0x61
	jne	.ret
	cmp	byte [rdi+6], 0x7b
	jne	.ret
	cmp	byte [rdi+21], 0x61
	jne	.ret
	cmp	byte [rdi+2], 0x70
	jne	.ret
	cmp	byte [rdi+34], 0x21
	jne	.ret
	cmp	byte [rdi+19], 0x31
	jne	.ret
	cmp	byte [rdi+29], 0x6c
	jne	.ret
	cmp	byte [rdi+28], 0x34
	jne	.ret
	cmp	byte [rdi+24], 0x5f
	jne	.ret
	cmp	byte [rdi+17], 0x31
	jne	.ret
	cmp	byte [rdi+25], 0x31
	jne	.ret
	cmp	byte [rdi+31], 0x34
	jne	.ret
	cmp	byte [rdi+11], 0x69
	jne	.ret
	cmp	byte [rdi+3], 0x61
	jne	.ret
	cmp	byte [rdi+27], 0x5f
	jne	.ret
	cmp	byte [rdi+7], 0x6b
	jne	.ret
	cmp	byte [rdi+22], 0x63
	jne	.ret

	mov	 eax, 1
.ret:
	ret
