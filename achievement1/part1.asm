;======================================
; Простой пример (Assembler для Atmega8)
;  С разделёнными векторами прерываний
;======================================
.include "m8def.inc"   ; Подключаем определения для ATmega8

.def  temp      = r16

;--------------------------------------
; Константы
.equ F_CPU      = 1000000      ; Частота (1 MHz)
.equ BAUD       = 9600
.equ UBRR_VALUE = (F_CPU/(16*BAUD))-1

.equ OCR1A_VAL  = 488

.equ OCR2_VAL   = 244

.cseg

.org 0x0000
    rjmp RESET 

.org OC2addr
    rjmp TIMER2_ISR

.org OC1Aaddr
    rjmp TIMER1_ISR


RESET:
    ldi temp, 0x00
    out DDRB, temp
    out DDRC, temp
    out DDRD, temp

    ldi temp, UBRR_VALUE
    out UBRRL, temp
    ldi temp, 0
    out UBRRH, temp
    ldi temp, (1<<RXEN)|(1<<TXEN)
    out UCSRB, temp
    ldi temp, (1<<URSEL)|(3<<UCSZ0)
    out UCSRC, temp

    ldi temp, high(OCR1A_VAL)
    out OCR1AH, temp
    ldi temp, low(OCR1A_VAL)
    out OCR1AL, temp

    ldi temp, (1<<WGM12)
    out TCCR1B, temp
    ldi temp, (1<<CS12)|(1<<CS10)
    out TCCR1B, temp

    ldi temp, (1<<OCIE1A)
    out TIMSK, temp

    ldi temp, OCR2_VAL
    out OCR2, temp
    ldi temp, (1<<WGM21)|(1<<CS22)|(1<<CS21)|(1<<CS20)
    out TCCR2, temp
    in temp, TIMSK
    ori temp, (1<<OCIE2)
    out TIMSK, temp

    sei

main_loop:
    rjmp main_loop


; Функции отправки в USART
send_char:
    sbis UCSRA, UDRE
    rjmp send_char
    out  UDR, r24           ; Отправка байта в R24
    ret

send_string:
next_char:
    lpm r24, Z+
    tst r24
    breq done_string
    rcall send_char
    rjmp next_char
done_string:
    ret

ping_str:
    .db "ping\r\n", 0

pong_str:
    .db "pong\r\n", 0


TIMER1_ISR:
    push r24
    push r25
    push ZH
    push ZL

    ldi r24, high(ping_str*2)
    ldi r25, low(ping_str*2)
    mov ZH, r24
    mov ZL, r25
    rcall send_string

    pop ZL
    pop ZH
    pop r25
    pop r24
    reti


TIMER2_ISR:
    push r24
    push r25
    push ZH
    push ZL

    ldi r24, high(pong_str*2)
    ldi r25, low(pong_str*2)
    mov ZH, r24
    mov ZL, r25
    rcall send_string

    pop ZL
    pop ZH
    pop r25
    pop r24
    reti