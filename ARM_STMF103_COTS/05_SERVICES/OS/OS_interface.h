/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:16 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef _OS_INTERFACE_H_
/*	define this file  */
#define _OS_INTERFACE_H_

typedef struct{
	u8	number;
	u16 priority;
	u16 priodicity;
	u16 firstDalay;
	void (*fptr) (void);
	u8	status;
}Task_t;

void SOS_voidStart			(void);
void SOS_voidCreateTask 	(Task_t * Copy_Task);
void SOS_voidDeleteTask 	(Task_t * Copy_Task);
void SOS_voidSuspendTask	(Task_t * Copy_Task);
void SOS_voidResumeTask		(Task_t * Copy_Task);

#endif 
