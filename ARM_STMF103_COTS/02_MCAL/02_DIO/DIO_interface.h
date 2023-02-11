/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:10 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef DIO_INTERFACE_H_
#define DIO_INTERFACE_H_

#define GPIO_PORTA	0
#define GPIO_PORTB	1
#define GPIO_PORTC	2
#define GPIO_PORTD	3
#define GPIO_PORTE	4
#define GPIO_PORTF	5
#define GPIO_PORTG	6

#define GPIO_PIN0	0
#define GPIO_PIN1	1
#define GPIO_PIN2	2
#define GPIO_PIN3	3
#define GPIO_PIN4	4
#define GPIO_PIN5	5
#define GPIO_PIN6	6
#define GPIO_PIN7	7
#define GPIO_PIN8	8
#define GPIO_PIN9	9
#define GPIO_PIN10	10
#define GPIO_PIN11	11
#define GPIO_PIN12	12
#define GPIO_PIN13	13
#define GPIO_PIN14	14
#define GPIO_PIN15	15

#define GPIO_PIN_HIGH	1
#define GPIO_PIN_LOW	0


/*		CCMM	
	C: configuretions
	M: Mode
	Modes:	
		00	input
		01	output@10MHz
		10	output@2MHz
		11	output@50MHz
	
	Configurations(output):
		00	Pushpull				PP
		01	Open Drain				OD
		10	Alternative Pushpull	AF_PP
		11	Alternative Open Drain	AF_OD
	
	Configurations(input):
		00	Analog		ANALOG
		01	Floating 	FLOATING
		10	Pulled		PULL_UP_DOWN
		11	reserved
*/
/*	Input Modes/Config	*/
#define GPIO_INPUT_ANALOG		0b0000
#define GPIO_INPUT_FLOATING		0b0100
#define GPIO_INPUT_PULL_UP_DOWN	0b1000

/*	Output Modes/Config	@ 10MHz	*/
#define GPIO_OUTPUT_10MHZ_PP		0b0001
#define GPIO_OUTPUT_10MHZ_OD		0b0101
#define GPIO_OUTPUT_10MHZ_AF_PP		0b1001
#define GPIO_OUTPUT_10MHZ_AF_OD		0b1101

/*	Output Modes/Config	@ 2MHz	*/
#define GPIO_OUTPUT_2MHZ_PP		0b0010
#define GPIO_OUTPUT_2MHZ_OD		0b0110
#define GPIO_OUTPUT_2MHZ_AF_PP	0b1010
#define GPIO_OUTPUT_2MHZ_AF_OD	0b1110

/*	Output Modes/Config	@ 50MHz	*/
#define GPIO_OUTPUT_50MHZ_PP		0b0011
#define GPIO_OUTPUT_50MHZ_OD		0b0111
#define GPIO_OUTPUT_50MHZ_AF_PP		0b1011
#define GPIO_OUTPUT_50MHZ_AF_OD		0b1111

void DIO_voidSetPinDirection	(u8 copy_u8Port, u8 copy_u8Pin, u8 copy_u8Mode);
void DIO_voidSetPinValue		(u8 copy_u8Port, u8 copy_u8Pin, u8 copy_u8Value);
u8 	 DIO_u8GetPinValue			(u8 copy_u8Port, u8 copy_u8Pin);

#endif

