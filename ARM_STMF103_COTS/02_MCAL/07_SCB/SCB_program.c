/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:14 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "SCB_interface.h"
#include "SCB_private.h"
#include "SCB_config.h"

void MSCB_voidInit(void){

#if		SCB_GROUP_SUB_SRTUCTURE == GROUP_4_SUB_0
	SCB_AIRCR = GROUP_4_SUB_0_KEY;
#elif	SCB_GROUP_SUB_SRTUCTURE == GROUP_3_SUB_1
	SCB_AIRCR = GROUP_3_SUB_1_KEY;
#elif	SCB_GROUP_SUB_SRTUCTURE == GROUP_2_SUB_2
	SCB_AIRCR = GROUP_2_SUB_2_KEY;
#elif	SCB_GROUP_SUB_SRTUCTURE == GROUP_1_SUB_3
	SCB_AIRCR = GROUP_1_SUB_3_KEY;
#elif	SCB_GROUP_SUB_SRTUCTURE == GROUP_0_SUB_4
	SCB_AIRCR = GROUP_0_SUB_4_KEY;
#else
#error "Wrong SCB_GROUP_SUB_SRTUCTURE configuration parameter"
#endif

}

void MSCB_voidSetPeriorityStructure	(u32 Copy_u32Structure){
	SCB_AIRCR = (SCB_AIRCR_KEY | Copy_u32Structure);
}
