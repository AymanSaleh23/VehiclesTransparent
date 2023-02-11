/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:14 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/
#ifndef SCB_INTERFACE_H_
#define SCB_INTERFACE_H_

#define SCB_GROUP_4_SUB_0	0x300
#define SCB_GROUP_3_SUB_1	0x400
#define SCB_GROUP_2_SUB_2	0x500
#define SCB_GROUP_1_SUB_3	0x600
#define SCB_GROUP_0_SUB_4	0x700

void MSCB_voidInit					(void);
void MSCB_voidSetPeriorityStructure	(u32 Copy_u32Structure);


#endif
