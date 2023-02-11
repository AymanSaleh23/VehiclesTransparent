/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:12 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef EXTI_INTERFACE_H_
#define EXTI_INTERFACE_H_

/*	Can be Enumerate but not Standard in C*/
#define EXTI_LINE_0	 0
#define EXTI_LINE_1  1
#define EXTI_LINE_2  2
#define EXTI_LINE_3  3

#define EXTI_LINE_4  4
#define EXTI_LINE_5  5
#define EXTI_LINE_6  6
#define EXTI_LINE_7  7

#define EXTI_LINE_8  8
#define EXTI_LINE_9  9
#define EXTI_LINE_10 10
#define EXTI_LINE_11 11

#define EXTI_LINE_12 12
#define EXTI_LINE_13 13
#define EXTI_LINE_14 14
#define EXTI_LINE_15 15

/*	EXTI number in Vector Taable at Core	*/
#define EXTI_IRQ_0	 6
#define EXTI_IRQ_1  7
#define EXTI_IRQ_2  8
#define EXTI_IRQ_3  9
#define EXTI_IRQ_4  10

#define EXTI_IRQ_5  23
#define EXTI_IRQ_6  23
#define EXTI_IRQ_7  23
#define EXTI_IRQ_8  23
#define EXTI_IRQ_9  23

#define EXTI_IRQ_10 40
#define EXTI_IRQ_11 40
#define EXTI_IRQ_12 40
#define EXTI_IRQ_13 40
#define EXTI_IRQ_14 40
#define EXTI_IRQ_15 40

/*	Sensitivity Choices	*/
#define EXTI_RISING_EDGE		0
#define	EXTI_FALLING_EDGE		1
#define	EXTI_ON_CHANGE			2

/*Line and Mode are parameters in define */
void MEXTI_voidInit 			(void);
void MEXTI_voidEnableEXTI 		(u8 Copy_u8Line);
void MEXTI_voidDisableEXTI 		(u8 Copy_u8Line);
void MEXTI_voidSWTrigger 		(u8 Copy_u8Line);
void MEXTI_voidSetSignalLatch	(u8 Copy_u8Line, u8 Copy_u8Mode);
void MEXTI_voidSetCallBack		(u8 Copy_u8Line, void (* ptr)(void) );
#endif
