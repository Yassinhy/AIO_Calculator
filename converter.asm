section .data
	input_number dq -2.4e2
	format db "%c%.12fx10^%lld", 10, 0  ;format for printing in base 10
	num dq 1.0                          ;used later

	table   dq 0.5
                dq 0.25
                dq 0.125
                dq 0.0625
                dq 0.03125
                dq 0.015625
                dq 0.0078125
                dq 0.00390625
                dq 0.001953125
                dq 0.0009765625
                dq 0.00048828125
                dq 0.000244140625
                dq 0.0001220703125
                dq 0.00006103515625
                dq 0.000030517578125
                dq 0.0000152587890625
                dq 0.00000762939453125
                dq 0.000003814697265625
                dq 0.0000019073486328125
                dq 0.00000095367431640625
                dq 0.000000476837158203125
                dq 0.0000002384185791015625
                dq 0.00000011920928955078125
                dq 0.000000059604644775390625
                dq 0.0000000298023223876953125
                dq 0.00000001490116119384765625
                dq 0.000000007450580596923828125
                dq 0.0000000037252902984619140625
                dq 0.00000000186264514923095703125
                dq 0.000000000931322574615478515625
                dq 0.0000000004656612873077392578125
                dq 0.00000000023283064365386962890625
                dq 0.000000000116415321826934814453125
                dq 0.0000000000582076609134674072265625
                dq 0.00000000002910383045673370361328125
                dq 0.000000000014551915228366851806640625
                dq 0.0000000000072759576141834259033203125
                dq 0.00000000000363797880709171295166015625
                dq 0.000000000001818989403545856475830078125
                dq 0.0000000000009094947017729282379150390625
                dq 0.00000000000045474735088646411895751953125
                dq 0.000000000000227373675443232059478759765625
                dq 0.0000000000001136868377216160297393798828125
                dq 0.00000000000005684341886080801486968994140625
                dq 0.000000000000028421709430404007434844970703125
                dq 0.0000000000000142108547152020037174224853515625
                dq 0.00000000000000710542735760100185871124267578125
                dq 0.000000000000003552713678800500929355621337890625
                dq 0.0000000000000017763568394002504646778106689453125
                dq 0.00000000000000088817841970012523233890533447265625
                dq 0.000000000000000444089209850062616169452667236328125	;52nd number


section .bss
	sign resb 1

section .text
	global _start
	extern printf


_start:
	;now we will extract the sign bit
        LEA rdi, [sign]
        MOV byte [rdi] , '+'
	BT qword[input_number], 63    ;store in carry flag 1 if the 63rd (first bit) is 1, and remove the 1 and make it 0
	JNC .skip
	MOV byte [rdi], '-'		;sign stored in SIGN

.skip:
	;now we get the exponent
	MOV rbx, [input_number]	       ;
	SHR rbx, 52
	AND rbx, 0b011111111111
	SUB rbx, 1023

	IMUL rbx, 19728
	SHR rbx, 16			;exponent stored in RBX

        MOVQ xmm0, qword[table + 8]

	MOVQ xmm0, qword [num]
	XOR rcx, rcx

	MOV rax, qword[input_number]
	AND rax, 0b0000000000001111111111111111111111111111111111111111111111111111

.loop:
	BT rax, 0
	JZ .next
	ADDPD xmm0, qword[table + 8 * rcx]

.next:
	ADD rcx, 1
	SHR rax, 1
	TEST rax, rax
	JNZ .loop











        MOV rdi, format
	MOVZX rsi, byte [sign]
	MOV rax, 1
	MOV rdx ,rbx
        CALL printf

        XOR rdi, rdi  ; Exit status = 0 (success)
        MOV rax, 60   ; Syscall number for exit
        SYSCALL       ; Exit the program
