
/******************************************************************************************/
/*******************************	Author : Ayman Saleh		***************************/
/*******************************	Date   : 9-10-2022			***************************/
/*******************************	Version: 1.0.0				***************************/
/*******************************	Layer  : HAL				***************************/
/*******************************	SWC    : SSD (7 segments)	***************************/
/******************************************************************************************/
/******************************************************************************************/


#ifndef SEG_INTERFACE_H_
#define SEG_INTERFACE_H_

#include "STD_TYPES.h"

#define SSD_u8_OUTSIDE_UC					20
#define SSD_u8_NO_COMMON_PIN_PORT_SUPPORTED	20

#define SSD_u8_COMMON_ANODE 		0
#define SSD_u8_COMMON_CATHODE 		1

#define SSD_u8_DEC					9
#define SSD_u8_HEX					15

typedef struct {
	u8 PORT;
	u8 CommonMode;
	u8 CommonPinPort;
	u8 CommonPin;
	u8 NumberSystem;
}SSD_type;

void SSD_voidInit	 	(const SSD_type* copy_u8SSDObject);
void SSD_voidSendNum 	(const SSD_type* copy_u8SSDObject , u8 copy_u8Number);
void SSD_voidOff	(const SSD_type* copy_u8SSDObject);
void SSD_voidOn		(const SSD_type* copy_u8SSDObject);

#endif
