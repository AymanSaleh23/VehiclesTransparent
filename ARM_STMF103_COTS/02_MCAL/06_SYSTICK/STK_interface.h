/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:12 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef STK_INTERFACE_H_
#define STK_INTERFACE_H_

void MSTK_voidInit					(void);
void MSTK_voidSetBusyWait			(u32 Copy_u32Ticks);
void MSTK_voidSetIntervalSingle		(u32 Copy_u32Ticks, void (*ptr) (void) );
void MSTK_voidSetIntervalPriodic	(u32 Copy_u32Ticks, void (*ptr) (void) );
void MSTK_voidStopInterval	(void);
u32 MSTK_u32ElapsedTime		(void);
u32 MSTK_u32RemainingTime	(void);


#endif
