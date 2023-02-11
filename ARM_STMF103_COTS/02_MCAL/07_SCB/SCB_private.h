/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:14 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/
#ifndef SCB_PRIVATE_H_
#define SCB_PRIVATE_H_

#define SCB_BASE_ADDRESS	0xE000ED00
#define SCB_AIRCR_KEY		0x05FA0000

#define SCB_AIRCR			*((volatile u32*) (SCB_BASE_ADDRESS	+ 0x0C))

#define GROUP_4_SUB_0		1
#define GROUP_3_SUB_1		2
#define GROUP_2_SUB_2		3
#define GROUP_1_SUB_3		4
#define GROUP_0_SUB_4		5

#define GROUP_4_SUB_0_KEY	0x05FA0300
#define GROUP_3_SUB_1_KEY	0x05FA0400
#define GROUP_2_SUB_2_KEY	0x05FA0500
#define GROUP_1_SUB_3_KEY	0x05FA0600
#define GROUP_0_SUB_4_KEY	0x05FA0700
#endif
