/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:14 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include 	"STD_TYPES.h"
#include 	"BIT_MATH.h"

#include 	"DIO_interface.h"
#include 	"STK_interface.h"

#include 	"LEDMRX_interface.h"
#include 	"LEDMRX_private.h"
#include 	"LEDMRX_config.h"

static u8 matrixCloumns[8][2]= {
		{LEDMRX_COLUMN_0},
		{LEDMRX_COLUMN_1},
		{LEDMRX_COLUMN_2},
		{LEDMRX_COLUMN_3},
		{LEDMRX_COLUMN_4},
		{LEDMRX_COLUMN_5},
		{LEDMRX_COLUMN_6},
		{LEDMRX_COLUMN_7}
};
static u8 matrixRows[8][2] = {
		{LEDMRX_ROW_0   },
		{LEDMRX_ROW_1   },
		{LEDMRX_ROW_2   },
		{LEDMRX_ROW_3   },
		{LEDMRX_ROW_4   },
		{LEDMRX_ROW_5   },
		{LEDMRX_ROW_6   },
		{LEDMRX_ROW_7   }
};

void HLEDMRX_voidInit(void){
	for (u8 i = 0 ; i < 8 ; i ++){
		DIO_voidSetPinDirection(matrixCloumns[i][0], matrixCloumns[i][1], GPIO_OUTPUT_2MHZ_PP);
		DIO_voidSetPinDirection(matrixRows[i][0]   , matrixRows[i][1]   , GPIO_OUTPUT_2MHZ_PP);
	}
	HLEDMRX_voidDisableAllColumns();
}

void HLEDMRX_voidDisplay( u8* Copy_u8ptrData){

	for (u8 i=0 ; i < 8; i ++){
		/*	Disable All Columns	*/
		HLEDMRX_voidDisableAllColumns();
		/*	Display each Row	*/
		HLEDMRX_voidDisplayRow(Copy_u8ptrData[i], i);
		/*	Busy Waiting		*/
		//MSTK_voidSetBusyWait(2500);
	}

}

static  void HLEDMRX_voidDisableAllColumns(void){
	for (u8 i = 0 ; i < 8 ; i ++){
		DIO_voidSetPinValue(matrixCloumns[i][0], matrixCloumns[i][1], GPIO_PIN_HIGH);
	}
}

static void HLEDMRX_voidDisplayRow(u8 Copy_u8RowValue,u8 Copy_u8Row){
	/*	Display Data	*/
	for (u8 i = 0 ; i < 8 ; i ++){
		DIO_voidSetPinValue(matrixRows[i][0], matrixRows[i][1], GET_BIT(Copy_u8RowValue, i) );
	}
	/*	Enable one Column	*/
	DIO_voidSetPinValue(matrixCloumns[Copy_u8Row][0], matrixCloumns[Copy_u8Row][1], GPIO_PIN_LOW);
}
