#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "DIO_interface.h"
#include "DIO_private.h"
#include "DIO_config.h"

void DIO_voidSetPinDirection	(u8 copy_u8Port, u8 copy_u8Pin, u8 copy_u8Mode){
	if (copy_u8Port <= GPIO_PORTG){
		switch (copy_u8Port){
		case GPIO_PORTA:{
			if (copy_u8Pin < GPIO_PIN8 ){
				GPIOA_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOA_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}
			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOA_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOA_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}
		}
		/*PORTA Case End*/
		break;
		case GPIO_PORTB:{
			if (copy_u8Pin < GPIO_PIN8 ){
				GPIOB_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOB_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}
			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOB_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOB_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}

		}
		/*PORTB Case End*/
		break;
		case GPIO_PORTC:{
			if (copy_u8Pin < GPIO_PIN8 ){
				GPIOC_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOC_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}

			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOC_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOC_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}
		}
		/*PORTC Case End*/
		break;

		case GPIO_PORTD:{
			if (copy_u8Pin < GPIO_PIN8 ){
				GPIOD_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOD_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}

			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOD_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOD_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}

		}
		/*PORTD Case End*/
		break;
		case GPIO_PORTE:{
			if (copy_u8Pin < GPIO_PIN8){
				GPIOE_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOE_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}

			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOE_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOE_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}

		}
		/*PORTE Case End*/
		break;
		case GPIO_PORTF:{
			if (copy_u8Pin < GPIO_PIN8 ){
				GPIOF_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOF_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}

			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOF_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOF_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}

		}
		/*PORTF Case End*/
		break;
		case GPIO_PORTG:{

			if (copy_u8Pin < GPIO_PIN8 ){
				GPIOG_CRL &= ~(DIO_MODE_CONFIG_MASK<< 4*copy_u8Pin);
				GPIOG_CRL |= (copy_u8Mode << 4*copy_u8Pin);
			}

			else if ((copy_u8Pin >= GPIO_PIN8) && (copy_u8Pin <= GPIO_PIN15) ){
				GPIOG_CRH &= ~(DIO_MODE_CONFIG_MASK<< 4*(copy_u8Pin-GPIO_PIN8));
				GPIOG_CRH |=  (copy_u8Mode << 4*(copy_u8Pin-GPIO_PIN8));
			}
			else {
				/*	Error_Wrong Pin	*/
			}
		}
		/*PORTG Case End*/
		break;

		}
	}
	else {
		//Error_Wrong Port
	}
}
void DIO_voidSetPinValue		(u8 copy_u8Port, u8 copy_u8Pin, u8 copy_u8Value){
	if (copy_u8Pin < 32){

		if (copy_u8Value == GPIO_PIN_HIGH){
			switch (copy_u8Port){
			case GPIO_PORTA:{
				SET_BIT(GPIOA_ODR, copy_u8Pin);
			}
			/*PORTA Case End*/
			break;
			case GPIO_PORTB:{
				SET_BIT(GPIOB_ODR, copy_u8Pin);
			}
			/*PORTB Case End*/
			break;
			case GPIO_PORTC:{
				SET_BIT(GPIOC_ODR, copy_u8Pin);
			}
			/*PORTC Case End*/
			break;
			case GPIO_PORTD:{
				SET_BIT(GPIOD_ODR, copy_u8Pin);
			}
			/*PORTD Case End*/
			break;
			case GPIO_PORTE:{
				SET_BIT(GPIOE_ODR, copy_u8Pin);
			}
			/*PORTE Case End*/
			break;
			case GPIO_PORTF:{
				SET_BIT(GPIOF_ODR, copy_u8Pin);
			}
			/*PORTF Case End*/
			break;
			case GPIO_PORTG:{
				SET_BIT(GPIOG_ODR, copy_u8Pin);
			}
			/*PORTG Case End*/
			break;

			}
		}
		else if (copy_u8Value == GPIO_PIN_LOW){

			switch (copy_u8Port){
			case GPIO_PORTA:{
				CLR_BIT(GPIOA_ODR, copy_u8Pin);
			}
			/*PORTA Case End*/
			break;
			case GPIO_PORTB:{
				CLR_BIT(GPIOB_ODR, copy_u8Pin);
			}
			/*PORTB Case End*/
			break;
			case GPIO_PORTC:{
				CLR_BIT(GPIOC_ODR, copy_u8Pin);
			}
			/*PORTC Case End*/
			break;
			case GPIO_PORTD:{
				CLR_BIT(GPIOD_ODR, copy_u8Pin);
			}
			/*PORTD Case End*/
			break;
			case GPIO_PORTE:{
				CLR_BIT(GPIOE_ODR, copy_u8Pin);
			}
			/*PORTE Case End*/
			break;
			case GPIO_PORTF:{
				CLR_BIT(GPIOF_ODR, copy_u8Pin);
			}
			/*PORTF Case End*/
			break;
			case GPIO_PORTG:{
				CLR_BIT(GPIOG_ODR, copy_u8Pin);
			}
			/*PORTG Case End*/
			break;
			}
		}
		else {
			/* Wrong_Value*/
		}
	}
	else {
		/* Wrong_Pin*/
	}
}
u8 	 DIO_u8GetPinValue			(u8 copy_u8Port, u8 copy_u8Pin){

	u8 LOC_u8Result = 0 ;

	if (copy_u8Pin < 32){

		switch (copy_u8Port){
		case GPIO_PORTA:{
			LOC_u8Result = GET_BIT(GPIOA_ODR, copy_u8Pin);
		}
		/*PORTA Case End*/
		break;
		case GPIO_PORTB:{
			LOC_u8Result = GET_BIT(GPIOB_ODR, copy_u8Pin);
		}
		/*PORTB Case End*/
		break;
		case GPIO_PORTC:{
			LOC_u8Result = GET_BIT(GPIOC_ODR, copy_u8Pin);
		}
		/*PORTC Case End*/
		break;
		case GPIO_PORTD:{
			LOC_u8Result = GET_BIT(GPIOD_ODR, copy_u8Pin);
		}
		/*PORTD Case End*/
		break;
		case GPIO_PORTE:{
			LOC_u8Result = GET_BIT(GPIOE_ODR, copy_u8Pin);
		}
		/*PORTE Case End*/
		break;
		case GPIO_PORTF:{
			LOC_u8Result = GET_BIT(GPIOF_ODR, copy_u8Pin);
		}
		/*PORTF Case End*/
		break;
		case GPIO_PORTG:{
			LOC_u8Result = GET_BIT(GPIOG_ODR, copy_u8Pin);
		}
		/*PORTG Case End*/
		break;
		}

	}
	else {
		/* Wrong_Pin*/
	}
	return LOC_u8Result;
}
