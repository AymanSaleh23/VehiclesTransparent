
#include	"STD_TYPES.h"
#include	"BIT_MATH.h"

#include	"OS_interface.h"
#include	"OS_private.h"
#include	"OS_config.h"

#include	"STK_interface.h"

static Task_t OSTasks [NUMBER_OF_TASK] = {NULL_PTR};
static u32 TickCount = 0;

void SOS_voidCreateTask (Task_t * Copy_Task){
	OSTasks[Copy_Task->number].priodicity 	= Copy_Task->priodicity;
	OSTasks[Copy_Task->number].fptr 		= Copy_Task->fptr;
	OSTasks[Copy_Task->number].number 		= Copy_Task->number;
	OSTasks[Copy_Task->number].priority 	= Copy_Task->priority;
	OSTasks[Copy_Task->number].firstDalay 	= Copy_Task->firstDalay;
	OSTasks[Copy_Task->number].status		= READY;
}

void SOS_voidSuspendTask	(Task_t * Copy_Task){
	OSTasks[Copy_Task->number].status	=	SUSPEND;
}

void SOS_voidResumeTask	(Task_t * Copy_Task){
	OSTasks[Copy_Task->number].status	=	READY;
}

void SOS_voidDeleteTask (Task_t * Copy_Task){
	OSTasks[Copy_Task->number].priodicity 	= 0;
	OSTasks[Copy_Task->number].fptr 		= NULL_PTR;
	OSTasks[Copy_Task->number].number 		= 0;
	OSTasks[Copy_Task->number].priority 	= 0;
	OSTasks[Copy_Task->number].firstDalay 	= 0;
	OSTasks[Copy_Task->number].status		= TERMINATED;
}
void SOS_voidStart(void){
	/*Timer Initialization*/
	MSTK_voidInit ();
	/*	Set Tick Time (1ms = 1000us)*/
	MSTK_voidSetIntervalPriodic(1000, SOS_voidSheduler);
}
/*	The ISR of every Tick	*/
static void SOS_voidSheduler (void){
	/*	Scan all Tasks to execute it depend on Priodicity	*/
	for (u8 i = 0 ; i < NUMBER_OF_TASK; i++){
		if ( (OSTasks[i].fptr != NULL_PTR)  && ( OSTasks[i].status == READY )){

			/*	Execute the i-th Task depend on its priodicity divisible by ticks	*/

			if ( ((TickCount%(OSTasks[i].priodicity))  ==  0)){
				/*	Callback the function of task*/
				OSTasks[i].fptr();
			}

		}
	}
	/*	Task iterator	*/
	TickCount++;	
}
