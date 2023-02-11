/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:12 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "STK_interface.h"
#include "STK_private.h"
#include "STK_config.h"

void (*CallBack) (void) ;
u8 Source = IDLE ;

void MSTK_voidInit		(void){
	/*	STK_SOURCE	Start check	*/
#if 	STK_SOURCE	== STK_SOURCE_AHB
	SET_BIT(STK_CTRL, STK_CTRL_CLKSOURCE);
#elif 	STK_SOURCE	== STK_SOURCE_AHB_DIV_8
	CLR_BIT(STK_CTRL, STK_CTRL_CLKSOURCE);
#else
#error "Wrong STK_SOURCE configuration parameter"
	/*	STK_SOURCE	End check	*/
#endif
	CLR_BIT(STK_CTRL, STK_CTRL_TICKINT);
	CLR_BIT(STK_CTRL, STK_CTRL_ENABLE);
	STK_LOAD = 0;
	STK_VAL = 0;
}

void MSTK_voidSetBusyWait	(u32 Copy_u32Ticks){
	/*	Put total ticks in Load register*/
	STK_LOAD = Copy_u32Ticks;
	/*	Enable STK to start*/
	SET_BIT(STK_CTRL, STK_CTRL_ENABLE);
	/*	Poll on Flag */
	while ( (GET_BIT(STK_CTRL,STK_CTRL_COUNTFLAG) == 0) );
}
void MSTK_voidSetIntervalSingle	(u32 Copy_u32Ticks, void (*ptr) (void) ){

	STK_LOAD= 0;
	STK_VAL = 0;

	/*	Put total ticks in Load register*/
	STK_LOAD = Copy_u32Ticks;
	/*	Enable STK to start*/
	SET_BIT(STK_CTRL, STK_CTRL_ENABLE);
	/*	Enable Interrupt	*/
	SET_BIT(STK_CTRL, STK_CTRL_TICKINT);
	/*	Global Variable to Drive ISR*/
	Source = SINGLE_SHOT ;
	/*Set adderss of Callback function*/
	CallBack = ptr;

}
void MSTK_voidSetIntervalPriodic(u32 Copy_u32Ticks, void (*ptr) (void) ){

	/*	Put total ticks in Load register*/
	STK_LOAD = Copy_u32Ticks;
	/*	Enable STK to start*/
	SET_BIT(STK_CTRL, STK_CTRL_ENABLE);
	/*	Enable Interrupt	*/
	SET_BIT(STK_CTRL, STK_CTRL_TICKINT);
	/*	Global Variable to Drive ISR*/

	Source = PERIODIC ;
	/*Set adderss of Callback function*/
	CallBack = ptr;
}

void MSTK_voidStopInterval	(void){
	CLR_BIT(STK_CTRL, STK_CTRL_ENABLE);
	/*	Disable Interrupt	*/
	CLR_BIT(STK_CTRL, STK_CTRL_TICKINT);
	STK_LOAD = 0;
	STK_VAL = 0;
}
u32 MSTK_u32ElapsedTime		(void){
	u32 Local_u32Elapsed;
	Local_u32Elapsed = (STK_LOAD - STK_VAL);
	return Local_u32Elapsed;
}
u32 MSTK_u32RemainingTime	(void){
	u32 Local_u32Remaining;
	Local_u32Remaining = STK_VAL;
	return Local_u32Remaining;
}

void SysTick_Handler(void){

	if (Source == SINGLE_SHOT){
		MSTK_voidStopInterval();
	}
	else if (Source == PERIODIC){
		/*	Do nothing */
	}
	CallBack();
}
