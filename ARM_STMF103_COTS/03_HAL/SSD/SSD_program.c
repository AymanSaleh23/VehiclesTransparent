/******************************************************************************************/
/******************************************************************************************/
/*******************************	Author : Ayman Saleh		***************************/
/*******************************	Date   : 9-10-2022			***************************/
/*******************************	Version: 1.0.0				***************************/
/*******************************	Layer  : HAL				***************************/
/*******************************	SWC    : SSD (7 segments)	***************************/
/******************************************************************************************/
/******************************************************************************************/


#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "DIO_interface.h"

#include "SSD_config.h"
#include "SSD_interface.h"
#include "SSD_private.h"

static u8 MaxNumber ;

void SSD_voidInit	 	(const SSD_type* copy_u8SSDObject){

	if (copy_u8SSDObject->PORT <= GPIO_PORTG){


		if (( copy_u8SSDObject->CommonPin <= GPIO_PIN15 ) && ( copy_u8SSDObject->CommonPinPort <= GPIO_PORTG) ){

			if (copy_u8SSDObject->CommonMode == SSD_u8_COMMON_CATHODE){
				DIO_voidSetPinValue( copy_u8SSDObject->CommonPinPort , copy_u8SSDObject->CommonPin , GPIO_PIN_LOW);
			}
			else if (copy_u8SSDObject->CommonMode == SSD_u8_COMMON_ANODE){
				DIO_voidSetPinValue( copy_u8SSDObject->CommonPinPort , copy_u8SSDObject->CommonPin , GPIO_PIN_HIGH);
			}
			else if (copy_u8SSDObject->CommonPin == SSD_u8_OUTSIDE_UC){
				//	Do Noting
			}
		}

		else {

		}
	}
	else{

	}

	if 	(copy_u8SSDObject->NumberSystem < SSD_u8_DEC ){
		MaxNumber = copy_u8SSDObject->NumberSystem;
	}
	else if ( copy_u8SSDObject->NumberSystem == SSD_u8_DEC ){
		MaxNumber = SSD_u8_DEC;
	}
	else if  ( copy_u8SSDObject->NumberSystem == SSD_u8_HEX){
		MaxNumber = SSD_u8_HEX;
	}
	else {

	}
}

void SSD_voidSendNum 	(const SSD_type* copy_u8SSDObject , u8 copy_u8Number){
	static u8 SSDNumbers [] = { SEG_0 ,SEG_1 ,SEG_2 ,SEG_3, SEG_4, SEG_5, SEG_6, SEG_7, SEG_8, SEG_9, SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F  };

	if (copy_u8Number >= copy_u8SSDObject->NumberSystem){

	}
	else if (copy_u8Number <= copy_u8SSDObject->NumberSystem){
		if ( copy_u8SSDObject->CommonMode == SSD_u8_COMMON_CATHODE){
			DIO_voidSetPortValue( copy_u8SSDObject->PORT , (SSDNumbers[copy_u8Number]) );
		}
		else if ( copy_u8SSDObject->CommonMode == SSD_u8_COMMON_ANODE){

			DIO_voidSetPortValue( copy_u8SSDObject->PORT , ~(SSDNumbers[copy_u8Number]) );
		}
	}
}


void SSD_voidOff	(const SSD_type* copy_u8SSDObject){
	if ( copy_u8SSDObject->CommonMode == SSD_u8_COMMON_CATHODE){
		DIO_voidSetPinValue( copy_u8SSDObject->CommonPinPort , copy_u8SSDObject->CommonPin , GPIO_PIN_HIGH );
	}
	else if ( copy_u8SSDObject->CommonMode == SSD_u8_COMMON_ANODE){
		DIO_voidSetPinValue( copy_u8SSDObject->CommonPinPort , copy_u8SSDObject->CommonPin , GPIO_PIN_LOW);
	}
}

void SSD_voidOn	(const SSD_type* copy_u8SSDObject){
	if ( copy_u8SSDObject->CommonMode == SSD_u8_COMMON_CATHODE){
		DIO_voidSetPinValue( copy_u8SSDObject->CommonPinPort , copy_u8SSDObject->CommonPin , GPIO_PIN_LOW );
	}
	else if ( copy_u8SSDObject->CommonMode == SSD_u8_COMMON_ANODE){
		DIO_voidSetPinValue( copy_u8SSDObject->CommonPinPort , copy_u8SSDObject->CommonPin , GPIO_PIN_HIGH );
	}
}
