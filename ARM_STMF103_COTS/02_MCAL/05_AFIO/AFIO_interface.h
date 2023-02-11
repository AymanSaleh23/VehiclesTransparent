/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:12 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef AFIO_INTERFACE_H_
#define AFIO_INTERFACE_H_

#define	AFIO_LINE0	0
#define	AFIO_LINE1	1
#define	AFIO_LINE2	2
#define	AFIO_LINE3	3
#define	AFIO_LINE4	4
#define	AFIO_LINE5	5
#define	AFIO_LINE6	6
#define	AFIO_LINE7	7
#define	AFIO_LINE8	8
#define	AFIO_LINE9	9
#define	AFIO_LINE10	10
#define	AFIO_LINE11	11
#define	AFIO_LINE12	12
#define	AFIO_LINE13	13
#define	AFIO_LINE14	14
#define	AFIO_LINE15	15

#define AFIO_PORTA	0b0000
#define AFIO_PORTB	0b0001
#define AFIO_PORTC	0b0010
#define AFIO_PORTD	0b0011
#define AFIO_PORTE	0b0100
#define AFIO_PORTF	0b0101
#define AFIO_PORTG	0b0110

void MAFIO_voidSetEXTIConfiguration(u8 Copy_u8Line, u8 Copy_u8PortMap);
#endif
