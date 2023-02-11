
/************************************************************/
/*					Author : Ayman Saleh					*/
/*					Date   : 22-9-2022						*/
/*					Version: 1.0.0							*/
/************************************************************/

#ifndef TFT_PRIVATE_H_
#define TFT_PRIVATE_H_

#define CMD_SLEEP_OUT		0x11
#define CMD_COLOR_MODE		0x3A
#define CMD_DISPLAY_ON		0x29
#define CMD_SET_X			0x2A
#define CMD_SET_Y			0x2B
#define CMD_WRITE			0x2C

#define PRMTR_COLOR_MODE_444	0x03
#define PRMTR_COLOR_MODE_565	0x05
#define PRMTR_COLOR_MODE_666	0x06


static void voidWriteCommand(u8 Copy_u8Command);
static void voidWriteData	(u8 Copy_u8Data);
#endif
