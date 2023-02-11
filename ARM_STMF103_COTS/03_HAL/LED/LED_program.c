/******************************************************************************************/
/******************************************************************************************/
/*******************************	Author : Ayman Saleh		***************************/
/*******************************	Date   : 10-9-2022			***************************/
/*******************************	Version: 1.0.0				***************************/
/*******************************	Layer  : HAL				***************************/
/*******************************	SWC    : LED				***************************/
/******************************************************************************************/
/******************************************************************************************/


#include "BIT_MATH.h"
#include "STD_TYPES.h"

#include "DIO_interface.h"

#include "LED_config.h"
#include "LED_private.h"
#include "LED_interface.h"



void LED_voidTurnOff(const LED_Type* LED_configuration){

	if (LED_configuration->PORT <= DIO_u8_PORTD ){
		if (LED_configuration->PIN <= DIO_u8_PIN7 ){
			DIO_voidSetPinValue(LED_configuration->PORT , LED_configuration->PIN , 1&(~(LED_configuration->MODE)) );
		}
		else {
			
		}
	}
	else {
		
	}
	
}

void LED_voidTurnOn	(const LED_Type* LED_configuration){
	
	if (LED_configuration->PORT <= DIO_u8_PORTD ){
		if (LED_configuration->PIN <= DIO_u8_PIN7 ){
			DIO_voidSetPinValue(LED_configuration->PORT , LED_configuration->PIN , (LED_configuration->MODE) );
		}
		else {
			
		}
	}
	else {
		
	}

}

void LED_voidTogg	(const LED_Type* LED_configuration ){
	DIO_voidToggPin(LED_configuration->PORT , LED_configuration->PIN);
}

