/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:11 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef NVIC_INTERFACE_H_
#define NVIC_INTERFACE_H_
typedef enum{
	NVIC_WWDG, NVIC_PVD, NVIC_TAMPER, NVIC_RTC, NVIC_FLASH, NVIC_RCC, NVIC_EXTI0, NVIC_EXTI1, NVIC_EXTI2, NVIC_EXTI3, NVIC_EXTI4
}NVIC_lines;

void MNVIC_voidEnableInterrupt 	(u8 Copy_u8IntNumber);

void MNVIC_voidDisableInterrupt (u8 Copy_u8IntNumber);

void MNVIC_voidSetPendingFlag	(u8 Copy_u8IntNumber);

void MNVIC_voidClearPendingFlag	(u8 Copy_u8IntNumber);

u8   MNVIC_u8GetActiveFlag		(u8 Copy_u8IntNumber);

void MNVIC_voidSetPriority		(u8 Copy_u8PeripheralIdx, u8 Copy_u8Priority);

void MNVIC_voidInit(void);

#endif
