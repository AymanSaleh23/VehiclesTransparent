/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:12 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef STK_PRIVATE_H_
#define STK_PRIVATE_H_

#define STK_BASE_ADDRESS	(0xE000E010)

#define STK_CTRL 			*((volatile u32 *) (STK_BASE_ADDRESS + 0x00))
#define STK_CTRL_ENABLE		0
#define STK_CTRL_TICKINT	1
#define STK_CTRL_CLKSOURCE	2
#define STK_CTRL_COUNTFLAG	16

#define STK_LOAD 			*((volatile u32 *) (STK_BASE_ADDRESS + 0x04))
#define STK_VAL 			*((volatile u32 *) (STK_BASE_ADDRESS + 0x08))

#define STK_SOURCE_AHB			1
#define STK_SOURCE_AHB_DIV_8	2

#define PERIODIC		1
#define SINGLE_SHOT		2
#define IDLE			3


#endif
