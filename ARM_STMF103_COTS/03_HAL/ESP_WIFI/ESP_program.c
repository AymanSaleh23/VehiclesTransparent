
/************************************************************/
/*					Author : Ayman Saleh					*/
/*					Date   : 25-9-2022						*/
/*					Version: 1.0.0							*/
/************************************************************/


#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "UART_interface.h"

#include "ESP_interface.h"
#include "ESP_private.h"
#include "ESP_config.h"

void HESP_voidInit(void){
	u8 LOC_u8Result = 0 ;
	/*	Disable Echo from ESP	*/
	MUART_voidTransmit("ATE0\r\n");

	while (LOC_u8Result == 0 ){
		/*	ESP as Station mode 	*/
		MUART_voidTransmit("AT+CWMODE=1\r\n");
		LOC_u8Result = ESP_u8ValidateCMD ();
	}
}



u8 ESP_u8ValidateCMD ( void ){

	u8 LOC_u8Response [100] = {0};
	LOC_u8Response = MUART_u8Receive();
	u8 LOC_u8Dummy = 0;
	u8 i = 0 ;
	u8 LOC_u8Result = 0;

	/*	While stops only when time out occurred	*/
	while (LOC_u8Response[i-1] != 255){
		LOC_u8Dummy	= MUART_u8Receive();
		LOC_u8Response [i] = LOC_u8Dummy;
		i++;
	}

	/*	Check OK response	*/
	if (LOC_u8Response[0] == 'O' && LOC_u8Response[1] =='K'){
		LOC_u8Result = 1;
	}
	return LOC_u8Result;
}

