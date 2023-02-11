/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:14 SEP 2022 							*/
/*	Version	:V02		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef EXTI_PRIVATE_H_
#define EXTI_PRIVATE_H_

#define EXTI_BASE_ADDRESS	(0x40010400)

typedef struct {
	volatile u32 IMR;		/*	Set interrupt Mask	*/
	volatile u32 EMR;		/*	Event Mask			*/
	volatile u32 RTSR;		/*	Set Rising Edge	as Sensitivity Mode		*/
	volatile u32 FTSR;		/*	Set Falling Edge as Sensitivity Mode	*/
	volatile u32 SWIER;		/*	Software Interrupt Trigger	*/
	volatile u32 PR;		/*	Pending	*/
}EXTI_t;

/*	Define Pointer to Struct	*/
#define EXTI ((volatile EXTI_t *)(EXTI_BASE_ADDRESS))

#define LINE0	0
#define LINE1	1
#define LINE2	2
#define LINE3	3
#define LINE4	4
#define LINE5	5
#define LINE6	6
#define LINE7	7
#define LINE8	8
#define LINE9	9
#define LINE10	10
#define LINE11	11
#define LINE12	12
#define LINE13	13
#define LINE14	14
#define LINE15	15

/*	Callback Default	*/
#define NULL		0

#define RISING     	1
#define FALLING     2
#define ON_CHANGE   3

#define ENABLE	1
#define DISABLE	2

#endif
