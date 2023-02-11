/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:12 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "EXTI_interface.h"
#include "EXTI_private.h"
#include "EXTI_config.h"

void (*EXTI_callback[16]) (void) ={NULL};
/*	Initialize all EXTI as defined 	*/
void MEXTI_voidInit 		(void)
{
	/*	Check EXTI_LINEx Parameters */
#if   EXTI_LINE0	== ENABLE

#if   EXTI_SENSE_MODE_LINE0 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_0);
#elif EXTI_SENSE_MODE_LINE0 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_0);
#elif EXTI_SENSE_MODE_LINE0 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_0);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_0);
#else
#error "Wrong EXTI_SENSE_MODE_LINE0 configuration parameter"
#endif

	SET_BIT(EXTI -> IMR, EXTI_LINE_0);

#elif EXTI_LINE0	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_0);
#else
#error "Wrong EXTI_LINE0 configuration Parameter"
#endif

#if   EXTI_LINE1	== ENABLE

#if   EXTI_SENSE_MODE_LINE1 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_1);
#elif EXTI_SENSE_MODE_LINE1 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_SENSE_MODE_LINE1);
#elif EXTI_SENSE_MODE_LINE1 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_1);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_1);
#else
#error "Wrong EXTI_SENSE_MODE_LINE1 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_1);

#elif EXTI_LINE1	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_1);
#else
#error "Wrong EXTI_LINE1 configuration Parameter"
#endif

#if   EXTI_LINE2	== ENABLE

#if   EXTI_SENSE_MODE_LINE2 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_2);
#elif EXTI_SENSE_MODE_LINE2 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_2);
#elif EXTI_SENSE_MODE_LINE2 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_2);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_2);
#else
#error "Wrong EXTI_SENSE_MODE_LINE2 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_2);
#elif EXTI_LINE2	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_2);
#else
#error "Wrong EXTI_LINE2 configuration Parameter"
#endif

#if   EXTI_LINE3	== ENABLE

#if   EXTI_SENSE_MODE_LINE3 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_3);
#elif EXTI_SENSE_MODE_LINE3 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_3);
#elif EXTI_SENSE_MODE_LINE3 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_3);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_3);
#else
#error "Wrong EXTI_SENSE_MODE_LINE3 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_3);
#elif EXTI_LINE3	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_3);
#else
#error "Wrong EXTI_LINE3 configuration Parameter"
#endif

#if   EXTI_LINE4	== ENABLE

#if   EXTI_SENSE_MODE_LINE4 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_4);
#elif EXTI_SENSE_MODE_LINE4 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_4);
#elif EXTI_SENSE_MODE_LINE4 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_4);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_4);
#else
#error "Wrong EXTI_SENSE_MODE_LINE4 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_4);
#elif EXTI_LINE4	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_4);
#else
#error "Wrong EXTI_LINE4 configuration Parameter"
#endif

#if   EXTI_LINE5	== ENABLE

#if   EXTI_SENSE_MODE_LINE5 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_5);
#elif EXTI_SENSE_MODE_LINE5 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_5);
#elif EXTI_SENSE_MODE_LINE5 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_5);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_5);
#else
#error "Wrong EXTI_SENSE_MODE_LINE5 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_5);
#elif EXTI_LINE5	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_5);
#else
#error "Wrong EXTI_LINE5 configuration Parameter"
#endif

#if   EXTI_LINE6	== ENABLE

#if   EXTI_SENSE_MODE_LINE6 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_6);
#elif EXTI_SENSE_MODE_LINE6 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_6);
#elif EXTI_SENSE_MODE_LINE6 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_6);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_6);
#else
#error "Wrong EXTI_SENSE_MODE_LINE6 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_6);
#elif EXTI_LINE6	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_6);
#else
#error "Wrong EXTI_LINE6 configuration Parameter"
#endif

#if   EXTI_LINE7	== ENABLE

#if   EXTI_SENSE_MODE_LINE7 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_7);
#elif EXTI_SENSE_MODE_LINE7 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_7);
#elif EXTI_SENSE_MODE_LINE7 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_7);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_7);
#else
#error "Wrong EXTI_SENSE_MODE_LINE7 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_7);
#elif EXTI_LINE7	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_7);
#else
#error "Wrong EXTI_LINE7 configuration Parameter"
#endif

#if   EXTI_LINE8	== ENABLE

#if   EXTI_SENSE_MODE_LINE8 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_8);
#elif EXTI_SENSE_MODE_LINE8 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_8);
#elif EXTI_SENSE_MODE_LINE8 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_8);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_8);
#else
#error "Wrong EXTI_SENSE_MODE_LINE8 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_8);
#elif EXTI_LINE8	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_8);
#else
#error "Wrong EXTI_LINE8 configuration Parameter"
#endif

#if   EXTI_LINE9	== ENABLE

#if   EXTI_SENSE_MODE_LINE9 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_9);
#elif EXTI_SENSE_MODE_LINE9 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_9);
#elif EXTI_SENSE_MODE_LINE9 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_9);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_9);
#else
#error "Wrong EXTI_SENSE_MODE_LINE9 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_9);
#elif EXTI_LINE9	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_9);
#else
#error "Wrong EXTI_LINE9 configuration Parameter"
#endif

#if   EXTI_LINE10	== ENABLE

#if   EXTI_SENSE_MODE_LINE10 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_10);
#elif EXTI_SENSE_MODE_LINE10 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_10);
#elif EXTI_SENSE_MODE_LINE10 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_10);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_10);
#else
#error "Wrong EXTI_SENSE_MODE_LINE10 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_10);
#elif EXTI_LINE10	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_10);
#else
#error "Wrong EXTI_LINE10 configuration Parameter"
#endif

#if   EXTI_LINE11	== ENABLE

#if   EXTI_SENSE_MODE_LINE11 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_11);
#elif EXTI_SENSE_MODE_LINE11 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_11);
#elif EXTI_SENSE_MODE_LINE11 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_11);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_11);
#else
#error "Wrong EXTI_SENSE_MODE_LINE11 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_11);
#elif EXTI_LINE11	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_11);
#else
#error "Wrong EXTI_LINE11 configuration Parameter"
#endif

#if   EXTI_LINE12	== ENABLE

#if   EXTI_SENSE_MODE_LINE12 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_12);
#elif EXTI_SENSE_MODE_LINE12 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_12);
#elif EXTI_SENSE_MODE_LINE12 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_12);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_12);
#else
#error "Wrong EXTI_SENSE_MODE_LINE12 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_12);
#elif EXTI_LINE12	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_12);
#else
#error "Wrong EXTI_LINE12 configuration Parameter"
#endif

#if   EXTI_LINE13	== ENABLE

#if   EXTI_SENSE_MODE_LINE13 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_13);
#elif EXTI_SENSE_MODE_LINE13 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_13);
#elif EXTI_SENSE_MODE_LINE13 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_13);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_13);
#else
#error "Wrong EXTI_SENSE_MODE_LINE13 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_13);
#elif EXTI_LINE13	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_13);
#else
#error "Wrong EXTI_LINE13 configuration Parameter"
#endif

#if   EXTI_LINE14	== ENABLE

#if   EXTI_SENSE_MODE_LINE14 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_14);
#elif EXTI_SENSE_MODE_LINE14 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_14);
#elif EXTI_SENSE_MODE_LINE14 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_14);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_14);
#else
#error "Wrong EXTI_SENSE_MODE_LINE14 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_14);
#elif EXTI_LINE14	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_14);
#else
#error "Wrong EXTI_LINE14 configuration Parameter"
#endif

#if   EXTI_LINE15	== ENABLE

#if   EXTI_SENSE_MODE_LINE15 == RISING
	SET_BIT(EXTI -> RTSR, EXTI_LINE_15);
#elif EXTI_SENSE_MODE_LINE15 == FALLING
	SET_BIT(EXTI -> FTSR, EXTI_LINE_15);
#elif EXTI_SENSE_MODE_LINE15 == ON_CHANGE
	SET_BIT(EXTI -> FTSR, EXTI_LINE_15);
	SET_BIT(EXTI -> RTSR, EXTI_LINE_15);
#else
#error "Wrong EXTI_SENSE_MODE_LINE15 configuration parameter"
#endif
	SET_BIT(EXTI -> IMR, EXTI_LINE_15);
#elif EXTI_LINE15	== DISABLE
	CLR_BIT(EXTI -> IMR, EXTI_LINE_15);
#else
#error "Wrong EXTI_LINE15 configuration Parameter"
#endif
}

/*Enable the external Interrupt from Copy_u8Line*/
void MEXTI_voidEnableEXTI 	(u8 Copy_u8EXTILine){
	SET_BIT(EXTI -> IMR, Copy_u8EXTILine);
}
/*Disable the external Interrupt from Copy_u8Line*/
void MEXTI_voidDisableEXTI 	(u8 Copy_u8EXTILine){
	CLR_BIT(EXTI -> IMR, Copy_u8EXTILine);
}
/*SW trigger Interrupt from Copy_u8Line*/
void MEXTI_voidSWTrigger 	(u8 Copy_u8EXTILine){
	/*	Fire interrupt by SW for test or debug*/
	SET_BIT(EXTI -> SWIER, Copy_u8EXTILine);
}/*	Runtine Change Configuration*/

/*Latch (change configuration) of external Interrupt from Copy_u8Line*/
void MEXTI_voidSetSignalLatch (u8 Copy_u8EXTILine, u8 Copy_u8EXTIMode){
	/*	Disable The EXTI Line Temporarily to change sensitivity */
	MEXTI_voidDisableEXTI(Copy_u8EXTILine);
	switch (Copy_u8EXTIMode){
	case RISING: {
		SET_BIT(EXTI -> RTSR, Copy_u8EXTILine);
		CLR_BIT(EXTI -> FTSR, Copy_u8EXTILine);

	}
	break;
	case FALLING: {
		CLR_BIT(EXTI -> RTSR, Copy_u8EXTILine);
		SET_BIT(EXTI -> FTSR, Copy_u8EXTILine);
	}
	break;
	case ON_CHANGE: {
		SET_BIT(EXTI -> FTSR, Copy_u8EXTILine);
		SET_BIT(EXTI -> RTSR, Copy_u8EXTILine);
	}
	break;
	}
	/*	re enable the EXTI Line	*/
	MEXTI_voidEnableEXTI(Copy_u8EXTILine);
}

void MEXTI_voidSetCallBack		(u8 Copy_u8EXTILine, void (* ptr)(void) ){
	EXTI_callback[Copy_u8EXTILine] = ptr;
}

void  EXTI0_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_0 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_0]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_0 );
	}
}


void  EXTI1_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_1 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_1 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_1 );
	}
}

void  EXTI2_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_2 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_2 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_2 );
	}
}

void  EXTI3_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_3 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_3 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_3 );
	}
}


void  EXTI4_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_4] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_4 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_4 );
	}
}


void  EXTI5_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_5 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_5 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_5 );
	}
}


void  EXTI6_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_6 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_6 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_6 );
	}
}


void  EXTI7_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_7 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_7 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_7 );
	}
}


void  EXTI8_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_8 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_8 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_8 );
	}
}


void  EXTI9_IRQHandler(void) {
	if (EXTI_callback[EXTI_LINE_9 ] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_9 ]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_9 );
	}
}


void  EXTI10_IRQHandler(void){
	if (EXTI_callback[EXTI_LINE_10] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_10]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_10);
	}
}


void  EXTI11_IRQHandler(void){
	if (EXTI_callback[EXTI_LINE_11] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_11]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_11);
	}
}


void  EXTI12_IRQHandler(void){
	if (EXTI_callback[EXTI_LINE_12] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_12]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_12);
	}
}


void  EXTI13_IRQHandler(void){
	if (EXTI_callback[EXTI_LINE_13] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_13]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_13);
	}
}


void  EXTI14_IRQHandler(void){
	if (EXTI_callback[EXTI_LINE_14] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_14]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_14);
	}
}


void  EXTI15_IRQHandler(void){
	if (EXTI_callback[EXTI_LINE_15] != NULL){
		/*Callback the function in app layer*/
		EXTI_callback[EXTI_LINE_15]();
		/* Clear Pending Flag */
		SET_BIT(EXTI -> PR,EXTI_LINE_15);
	}
}
