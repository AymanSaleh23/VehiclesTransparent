/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:11 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "NVIC_interface.h"
#include "NVIC_private.h"
#include "NVIC_config.h"

#include "SCB_interface.h"
void MNVIC_voidInit(void){

	MSCB_voidInit();
}
void MNVIC_voidEnableInterrupt (u8 Copy_u8IntNumber){
	/*	Validata Interrupt Number	*/
	if (Copy_u8IntNumber < 32){
		/*	Call NVIC_ISER 0*/
		//SET_BIT has read-modify-write
		//SET_BIT(NVIC_ISER0, Copy_u8IntNumber);
		//prefere to directly assign the value to that bit hence 0 has no effect
		NVIC_ISER0 = (1<< Copy_u8IntNumber);
	}
	else if (Copy_u8IntNumber < 64){
		/*	Call NVIC_ISER 1*/
		NVIC_ISER1 = (1<< (Copy_u8IntNumber-32));
	}
	else {
		/*invalid interrupt Number*/
	}
}

void MNVIC_voidDisableInterrupt (u8 Copy_u8IntNumber){
	/*	Validata Interrupt Number	*/
	if (Copy_u8IntNumber < 32){
		/*	Call NVIC_ICER 0*/
		//SET_BIT has read-modify-write
		//SET_BIT(NVIC_ICER0, Copy_u8IntNumber);
		//prefere to directly assign the value to that bit hence 0 has no effect
		NVIC_ICER0 = (1<< Copy_u8IntNumber);
	}
	else if (Copy_u8IntNumber < 64){
		/*	Call NVIC_ICER 1*/
		NVIC_ICER1 = (1<< (Copy_u8IntNumber-32));
	}
	else {
		/*invalid interrupt Number*/
	}
}

void MNVIC_voidSetPendingFlag	(u8 Copy_u8IntNumber){

	/*	Validata Interrupt Number	*/
	if (Copy_u8IntNumber < 32){
		/*	Call NVIC_ISPR 0*/
		//SET_BIT has read-modify-write
		//SET_BIT(NVIC_ISPR0, Copy_u8IntNumber);
		//prefere to directly assign the value to that bit hence 0 has no effect
		NVIC_ISPR0 = (1<< Copy_u8IntNumber);
	}
	else if (Copy_u8IntNumber < 64){
		/*	Call NVIC_ISPR 1*/
		NVIC_ISPR1 = (1<< (Copy_u8IntNumber-32));
	}
	else {
		/*invalid interrupt Number*/
	}

}

void MNVIC_voidClearPendingFlag	(u8 Copy_u8IntNumber){
	/*	Validata Interrupt Number	*/
	if (Copy_u8IntNumber < 32){
		/*	Call NVIC_ICPR 0*/
		//SET_BIT has read-modify-write
		//SET_BIT(NVIC_ICPR0, Copy_u8IntNumber);
		//prefere to directly assign the value to that bit hence 0 has no effect
		NVIC_ICPR0 = (1<< Copy_u8IntNumber);
	}
	else if (Copy_u8IntNumber < 64){
		/*	Call NVIC_ICPR 1*/
		NVIC_ICPR1 = (1<< (Copy_u8IntNumber-32));
	}
	else {
		/*invalid interrupt Number*/
	}

}

u8   MNVIC_u8GetActiveFlag		(u8 Copy_u8IntNumber){
	u8 Local_u8Result;
	/*	Validata Interrupt Number	*/
	if (Copy_u8IntNumber < 32){
		Local_u8Result = GET_BIT(NVIC_IABR0, Copy_u8IntNumber);
	}
	else if (Copy_u8IntNumber < 64){
		Local_u8Result = GET_BIT(NVIC_IABR0, (Copy_u8IntNumber-32));
	}
	else {
		/*invalid interrupt Number*/
	}
	return Local_u8Result;
}

void MNVIC_voidSetPriority	(u8 Copy_u8PeripheralIdx, u8 Copy_u8Priority){
	NVIC_IPR[Copy_u8PeripheralIdx] = (Copy_u8Priority<<5);
}
