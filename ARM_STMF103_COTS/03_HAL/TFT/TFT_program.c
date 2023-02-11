
/************************************************************/
/*					Author : Ayman Saleh					*/
/*					Date   : 22-9-2022						*/
/*					Version: 1.0.0							*/
/************************************************************/


#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "DIO_interface.h"
#include "SPI_interface.h"
#include "STK_interface.h"

#include "TFT_interface.h"
#include "TFT_private.h"
#include "TFT_config.h"

void HTFT_voidInit		(void){
	/*	Reset Pulse	*/
	DIO_voidSetPinValue	(TFT_RST_PIN, GPIO_PIN_HIGH);
	MSTK_voidSetBusyWait(100);
	DIO_voidSetPinValue	(TFT_RST_PIN, GPIO_PIN_LOW);
	MSTK_voidSetBusyWait(1);
	DIO_voidSetPinValue	(TFT_RST_PIN, GPIO_PIN_HIGH);
	MSTK_voidSetBusyWait(100);
	DIO_voidSetPinValue	(TFT_RST_PIN, GPIO_PIN_LOW);
	MSTK_voidSetBusyWait(1);
	DIO_voidSetPinValue	(TFT_RST_PIN, GPIO_PIN_HIGH);
	MSTK_voidSetBusyWait(140000);

	/*	Sleep Out Command	*/
	voidWriteCommand(CMD_SLEEP_OUT);
	MSTK_voidSetBusyWait(150000);

	/*	Color Out Command	*/
	voidWriteCommand(CMD_COLOR_MODE);
	voidWriteData	(PRMTR_COLOR_MODE_565);

	/*	Display On Command	*/
	voidWriteCommand(CMD_DISPLAY_ON);
}
void HTFT_voidDisplayImg(const u16* Copy_pu16Img){

	u16 counter , LOC_u16TotalPixels = TFT_MAX_X * TFT_MAX_Y ;
	/*	Set X address	*/
	voidWriteCommand(CMD_SET_X);
	/*	Starting X  = 0	*/
	voidWriteData(0);
	voidWriteData(0);
	/*	Ending X  = 127	*/
	voidWriteData(0);
	voidWriteData(127);

	/*	Set Y address	*/
	voidWriteCommand(CMD_SET_Y);
	/*	Starting Y  = 0	*/
	voidWriteData(0);
	voidWriteData(0);
	/*	Ending Y  = 160	*/
	voidWriteData(0);
	voidWriteData(159);

	/*	RAM Write */
	voidWriteCommand(CMD_WRITE);

	for (counter = 0 ; counter < LOC_u16TotalPixels ; counter++){
		voidWriteData(Copy_pu16Img[counter] >> 8	);
		voidWriteData(Copy_pu16Img[counter] & 0x00ff);
	}
}

void HTFT_voidFillColor(u16	 Copy_u16Color){

	u16 counter , LOC_u16TotalPixels = TFT_MAX_X * TFT_MAX_Y ;
	/*	Set X address	*/
	voidWriteCommand(CMD_SET_X);
	/*	Starting X  = 0	*/
	voidWriteData(0);
	voidWriteData(0);
	/*	Ending X  = 127	*/
	voidWriteData(0);
	voidWriteData(127);

	/*	Set Y address	*/
	voidWriteCommand(CMD_SET_Y);
	/*	Starting Y  = 0	*/
	voidWriteData(0);
	voidWriteData(0);
	/*	Ending Y  = 160	*/
	voidWriteData(0);
	voidWriteData(159);

	/*	RAM Write */
	voidWriteCommand(CMD_WRITE);

	for (counter = 0 ; counter < LOC_u16TotalPixels ; counter++){
		voidWriteData(Copy_u16Color >> 8	);
		voidWriteData(Copy_u16Color & 0x00ff);
	}
}

void HTFT_voidDrawRectangle (u8 x1, u8 x2, u8 y1, u8 y2 ,u16 Copy_u16BorderColor){

	if ((x2 > x1) && ( y2 > y1 ) && ( (x2-x1) < TFT_MAX_X ) && ( (y2-y1) < TFT_MAX_Y ) ){
		u16 counter ;
		u16 size = (x2-x1)*(y2-y1);
		/*	Set X address	*/
		voidWriteCommand(CMD_SET_X);
		/*	Starting X	*/
		voidWriteData(0);
		voidWriteData(x1);
		/*	Ending X  	*/
		voidWriteData(0);
		voidWriteData(x2);

		/*	Set Y address	*/
		voidWriteCommand(CMD_SET_Y);
		/*	Starting Y 	*/
		voidWriteData(0);
		voidWriteData(y1);
		/*	Ending Y 	*/
		voidWriteData(0);
		voidWriteData(y2);

		/*	RAM Write */
		voidWriteCommand(CMD_WRITE);

		for (counter = 0 ; counter < size ; counter++){
			voidWriteData(Copy_u16BorderColor >> 8	);
			voidWriteData(Copy_u16BorderColor & 0x00ff);
		}
	}
	else {
		/*	Invalid X or Y*/
	}

}

static void voidWriteCommand(u8 Copy_u8Command){
	u16 LOC_u16Temp;
	/*	Apply Logic 0 to A0 of TFT to send Command	*/
	DIO_voidSetPinValue			( TFT_A0_PIN, GPIO_PIN_LOW);
	MSPI1_voidSendReceiveSynch	( Copy_u8Command, &LOC_u16Temp );
}
static void voidWriteData	(u8 Copy_u8Data){
	u16 LOC_u16Temp;
	/*	Apply Logic 1 to A0 of TFT to send Data		*/
	DIO_voidSetPinValue(TFT_A0_PIN, GPIO_PIN_HIGH);
	MSPI1_voidSendReceiveSynch(Copy_u8Data, &LOC_u16Temp );
}
