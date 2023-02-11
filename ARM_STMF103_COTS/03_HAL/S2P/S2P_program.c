
/****************************************************************************/
/*						Author : Ayman Saleh								*/
/*						Date   : 19-9-2022									*/
/*						Version: 1.0.0										*/
/****************************************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "DIO_interface.h"
#include "STK_interface.h"

#include "S2P_interface.h"
#include "S2P_private.h"
#include "S2P_config.h"

void HS2P_voidSendData	(u32 Copy_u32Data, u8 Copy_u8Length){
	u8 LOC_u8DataBit ;
	for (s8 i = Copy_u8Length ; i >=0 ; i--){
		LOC_u8DataBit = GET_BIT(Copy_u32Data,i);
		/*	Put data on Serial Data pin	*/
		DIO_voidSetPinValue	(SERIAL_DATA, LOC_u8DataBit);
		/*	Apply Pulse in Shift Clock	pin	*/

		DIO_voidSetPinValue	(SHIFT_CLK , GPIO_PIN_HIGH);
		MSTK_voidSetBusyWait(1);
		DIO_voidSetPinValue	(SHIFT_CLK , GPIO_PIN_LOW);
		MSTK_voidSetBusyWait(1);
	}
	/*	After 8 times Apply Clock pulse on Storage Clock Pin	*/
	/*	Apply Pulse in Shift Clock	pin	*/
	DIO_voidSetPinValue	(STORAGE_CLK , GPIO_PIN_HIGH);
	MSTK_voidSetBusyWait(1);
	DIO_voidSetPinValue	(STORAGE_CLK , GPIO_PIN_LOW);
	MSTK_voidSetBusyWait(1);


}
