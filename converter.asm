section .data
	input_number dq 0b1101100000001001001000011111101101010100010111010101111001110011

	num dq 1.0

	format db "%c%.12f", 10, 0

	table   dq 0.5			;this is a look up table for 2^-(1 through 52) to calculate the mantissa quickly and efficiently
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
	;the input number will be in rax for all use
	MOV rax, [input_number]

	;extract the sign bit
	MOV byte [sign], '+'				;move the '+' sign as the default
	BT rax, 63					;test the first bit in the input number
	JNC .sign_done
	MOV byte [sign], '-'

.sign_done:
	;now lets extract the exponent
	MOV r9, rax
	SHR r9, 52					;mask the mantissa
	AND r9, 0b011111111111				;mask the sign bit
	SUB r9, 1023					;the exponent is now stored in r9

	JMP .calculate_mantissa				;go to calculate the mantissa

.calculate_mantissa:

	;mask mantissa
	MOV rdx, 0x000FFFFFFFFFFFFF
	AND rax, rdx

	;initialize Xmm0
	MOVSD xmm0, [num]

	;loop
	MOV rcx, 52

.translate:
	MOV rdx, rcx 					;rdx contains the value from table
	SHL rdx, 3
	MOVSD xmm1, qword [table + rdx]
	TEST rax, 1					;if LSB == 1
	JZ .skip_addition
	ADDSD xmm0, xmm1

.skip_addition:
	SHR rax, 1					;shift to the next bit
	DEC rcx
	JNZ .translate					;loop if rcx != 0

.print_and_end:
	;print
	MOV rdi, format
	MOVZX rsi, byte [sign]				;first arg: the sign
;	MOV rdx, r9					;### arg: the exponent
	MOVSD xmm1, xmm0
	MOV rax, 1
	CALL printf

	;exit
	MOV rax, 60
	XOR rdi, rdi
	SYSCALL
