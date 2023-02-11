/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:18 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "DMA_interface.h"
#include "DMA_private.h"
#include "DMA_config.h"

static void (* DMA1_CallBack [DMA_1_MAX_CHANNEL] )(void) = {NULL_PTR};
static void (* DMA2_CallBack [DMA_2_MAX_CHANNEL] )(void) = {NULL_PTR};

void MDMA_voidChannelInit			(void){
	/*	Put The Configurations	*/
}

void MDMA_voidChannelStartRequest	( DMA_ChannelReq_t * Copy_DMAReq){
	if (Copy_DMAReq != NULL_PTR){
		if ((Copy_DMAReq->DMA_module == DMA_MODULE_1) && ( Copy_DMAReq->Channel <= DMA_1_MAX_CHANNEL )){
			/*	Disable Channel	*/
			DMA_1->Channel[Copy_DMAReq->Channel-1].CCRx.Channel_EN =  0 ;

			/*	Write Address	*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].DMA_CPAR = Copy_DMAReq->pu32DestinationAddress;
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].DMA_CMAR = Copy_DMAReq->pu32SourceAddress;

			/*	Block Size		*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].DMA_CNDTR = Copy_DMAReq->BlockLenght;

			/*	Set Priority	*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_PL = Copy_DMAReq->Priority;

			/*	Direction		*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_DIR =	Copy_DMAReq->Direction;
			if (Copy_DMAReq->Direction == DMA_READ_FROM_MEMORY){
				DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_MEM2MEM = READ_FORM_MEMORY_ENABLE;
			}
			else if (Copy_DMAReq->Direction == DMA_READ_FROM_PERIPHERAL){
				DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_MEM2MEM = READ_FORM_MEMORY_DISABLE;
			}

			/*	Memory & Peripheral Increment	*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_MINC	= Copy_DMAReq->MemoryInc;
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_PINC	= Copy_DMAReq->PeripheralInc;

			/*	Memory & Peripheral Size		*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_MSIZE = Copy_DMAReq->MemorySize;
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_PSIZE = Copy_DMAReq->PeripheralSize;

			/*	Circular Mode	*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_CIRC 	= Copy_DMAReq->CircularOperation;
			if ((Copy_DMAReq->fptr) != NULL_PTR){
				DMA1_CallBack[(Copy_DMAReq->Channel)-1] = Copy_DMAReq->fptr;
			}
			/*	Enable Interrupt*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TCIE	= 1;
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TEIE	= 1;

			/*	Enable Channel	*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_EN	= 1;
		}
		else if ((Copy_DMAReq->DMA_module == DMA_MODULE_2) && ( Copy_DMAReq->Channel <= DMA_2_MAX_CHANNEL )){
			/*	Disable Channel	*/
			DMA_2->Channel[Copy_DMAReq->Channel-1].CCRx.Channel_EN	= 0 ;

			/*	Write Address	*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].DMA_CPAR = Copy_DMAReq->pu32DestinationAddress;
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].DMA_CMAR = Copy_DMAReq->pu32SourceAddress;

			/*	Block Size		*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].DMA_CNDTR= Copy_DMAReq->BlockLenght;

			/*	Set Priority	*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_PL = Copy_DMAReq->Priority;

			/*	Direction		*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_DIR =	Copy_DMAReq->Direction;

			/*	Memory & Peripheral Increment	*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_MINC	= Copy_DMAReq->MemoryInc;
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_PINC	= Copy_DMAReq->PeripheralInc;

			/*	Memory & Peripheral Size		*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_MSIZE = Copy_DMAReq->MemorySize;
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_PSIZE = Copy_DMAReq->PeripheralSize;

			/*	Circular Mode	*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_CIRC 	= Copy_DMAReq->CircularOperation;
			if ((Copy_DMAReq->fptr) != NULL_PTR){
				DMA2_CallBack[(Copy_DMAReq->Channel)-1] = Copy_DMAReq->fptr;
			}
			/*	Enable Interrupt*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TCIE	= 1;
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TEIE	= 1;

			/*	Enable Channel	*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_EN	= 1;
		}
		else {
			/*	Invalid DMA module	*/
		}
	}
	else {
		/*	Invalid Pointer Input parameter	*/
	}

}
void MDMA_voidChannelNewOrder		( DMA_ChannelReq_t * Copy_DMAReq , u32 Copy_u32NewSource, u32 Copy_u32NewDestination ){
	if (Copy_DMAReq != NULL_PTR){
		if ((Copy_DMAReq->DMA_module == DMA_MODULE_1) && ( Copy_DMAReq->Channel <= DMA_1_MAX_CHANNEL )){
			/*	Disable Channel	*/
			CLR_BIT( DMA_1->Channel[Copy_DMAReq->Channel-1].CCRx.Channel_EN, 0 );

			/*	Disable Interrupt*/
			CLR_BIT(DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TCIE	,0);
			CLR_BIT(DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TEIE	,0);

			/*	Write Address	*/
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].DMA_CPAR = Copy_DMAReq->pu32DestinationAddress;
			DMA_1->Channel[(Copy_DMAReq->Channel)-1].DMA_CMAR = Copy_DMAReq->pu32SourceAddress;

			/*	Enable Interrupt*/
			SET_BIT(DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TCIE	,0);
			SET_BIT(DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TEIE	,0);

			/*	Enable Channel	*/
			SET_BIT(DMA_1->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_EN	,0);
		}
		else if ((Copy_DMAReq->DMA_module == DMA_MODULE_2) && ( Copy_DMAReq->Channel <= DMA_2_MAX_CHANNEL )){
			/*	Disable Channel	*/
			CLR_BIT( DMA_2->Channel[Copy_DMAReq->Channel-1].CCRx.Channel_EN, 0 );

			/*	Disable Interrupt*/
			CLR_BIT(DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TCIE	,0);
			CLR_BIT(DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TEIE	,0);

			/*	Write Address	*/
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].DMA_CPAR = Copy_DMAReq->pu32DestinationAddress;
			DMA_2->Channel[(Copy_DMAReq->Channel)-1].DMA_CMAR = Copy_DMAReq->pu32SourceAddress;

			/*	Enable Interrupt*/
			SET_BIT(DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TCIE	,0);
			SET_BIT(DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_TEIE	,0);

			/*	Enable Channel	*/
			SET_BIT(DMA_2->Channel[(Copy_DMAReq->Channel)-1].CCRx.Channel_EN	,0);
		}
		else {
			/*	Invalid DMA module	*/
		}
	}
	else {
		/*	Invalid Pointer Input parameter	*/
	}
}
u8	MDMA_u8GetFlag	( DMA_ChannelReq_t * Copy_DMAReq, u8 Copy_u8Flag){
	u8 LOC_u8Flag;
	if (Copy_DMAReq != NULL_PTR){
		if ((Copy_DMAReq->DMA_module == DMA_MODULE_1) && ( Copy_DMAReq->Channel <= DMA_1_MAX_CHANNEL )){
			switch (Copy_u8Flag){
			case DMA_GIF	:{LOC_u8Flag = GET_BIT(DMA_1->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_GIFx ) ) ; }break;
			case DMA_TCIF   :{LOC_u8Flag = GET_BIT(DMA_1->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_TCIFx) ) ; }break;
			case DMA_HTIF   :{LOC_u8Flag = GET_BIT(DMA_1->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_HTIFx) ) ; }break;
			case DMA_TEIF   :{LOC_u8Flag = GET_BIT(DMA_1->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_TEIFx) ) ; }break;
			}
		}
		else if ((Copy_DMAReq->DMA_module == DMA_MODULE_2) && ( Copy_DMAReq->Channel <= DMA_2_MAX_CHANNEL )){
			switch (Copy_u8Flag){
			case DMA_GIF	:{LOC_u8Flag = GET_BIT(DMA_2->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_GIFx ) ) ; }break;
			case DMA_TCIF   :{LOC_u8Flag = GET_BIT(DMA_2->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_TCIFx) ) ; }break;
			case DMA_HTIF   :{LOC_u8Flag = GET_BIT(DMA_2->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_HTIFx) ) ; }break;
			case DMA_TEIF   :{LOC_u8Flag = GET_BIT(DMA_2->DMA_ISR,( ( 4 * (Copy_DMAReq->Channel-1) ) + DMA_ISR_TEIFx) ) ; }break;
			}

		}
	}
	else {
		/*	Invalid Pointer Input parameter	*/
	}
	return LOC_u8Flag;
}
void DMA1_Channel1_IRQHandler(void){
	if (DMA1_CallBack[0] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 0);
		CLR_BIT((DMA_1->DMA_IFCR), 1);
		CLR_BIT((DMA_1->DMA_IFCR), 2);
		CLR_BIT((DMA_1->DMA_IFCR), 3);
		DMA1_CallBack[0]();
	}
	else {

	}
}
void DMA1_Channel2_IRQHandler(void){
	if (DMA1_CallBack[1] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 4);
		CLR_BIT((DMA_1->DMA_IFCR), 5);
		CLR_BIT((DMA_1->DMA_IFCR), 6);
		CLR_BIT((DMA_1->DMA_IFCR), 7);
		DMA1_CallBack[1]();
	}
	else {

	}
}
void DMA1_Channel3_IRQHandler(void){
	if (DMA1_CallBack[2] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 8);
		CLR_BIT((DMA_1->DMA_IFCR), 9);
		CLR_BIT((DMA_1->DMA_IFCR), 10);
		CLR_BIT((DMA_1->DMA_IFCR), 11);
		DMA1_CallBack[2]();
	}
	else {

	}
}
void DMA1_Channel4_IRQHandler(void){
	if (DMA1_CallBack[3] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 12);
		CLR_BIT((DMA_1->DMA_IFCR), 13);
		CLR_BIT((DMA_1->DMA_IFCR), 14);
		CLR_BIT((DMA_1->DMA_IFCR), 15);
		DMA1_CallBack[3]();
	}
	else {

	}
}
void DMA1_Channel5_IRQHandler(void){
	if (DMA1_CallBack[4] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 16);
		CLR_BIT((DMA_1->DMA_IFCR), 17);
		CLR_BIT((DMA_1->DMA_IFCR), 18);
		CLR_BIT((DMA_1->DMA_IFCR), 19);
		DMA1_CallBack[4]();
	}
	else {

	}

}
void DMA1_Channel6_IRQHandler(void){
	if (DMA1_CallBack[5] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 20);
		CLR_BIT((DMA_1->DMA_IFCR), 21);
		CLR_BIT((DMA_1->DMA_IFCR), 22);
		CLR_BIT((DMA_1->DMA_IFCR), 23);
		DMA1_CallBack[5]();
	}
	else {

	}
}
void DMA1_Channel7_IRQHandler(void){
	if (DMA1_CallBack[6] != NULL_PTR){
		CLR_BIT((DMA_1->DMA_IFCR), 24);
		CLR_BIT((DMA_1->DMA_IFCR), 25);
		CLR_BIT((DMA_1->DMA_IFCR), 26);
		CLR_BIT((DMA_1->DMA_IFCR), 27);
		DMA1_CallBack[6]();
	}
	else {

	}
}
void DMA2_Channel1_IRQHandler(void){
	if (DMA2_CallBack[0] != NULL_PTR){
		CLR_BIT((DMA_2->DMA_IFCR), 0);
		CLR_BIT((DMA_2->DMA_IFCR), 1);
		CLR_BIT((DMA_2->DMA_IFCR), 2);
		CLR_BIT((DMA_2->DMA_IFCR), 3);
		DMA2_CallBack[0]();
	}
	else {

	}
}
void DMA2_Channel2_IRQHandler(void){
	if (DMA2_CallBack[1] != NULL_PTR){
		CLR_BIT((DMA_2->DMA_IFCR), 4);
		CLR_BIT((DMA_2->DMA_IFCR), 5);
		CLR_BIT((DMA_2->DMA_IFCR), 6);
		CLR_BIT((DMA_2->DMA_IFCR), 7);
		DMA2_CallBack[1]();
	}
	else {

	}
}
void DMA2_Channel3_IRQHandler(void){
	if (DMA2_CallBack[2] != NULL_PTR){
		CLR_BIT((DMA_2->DMA_IFCR), 8);
		CLR_BIT((DMA_2->DMA_IFCR), 9);
		CLR_BIT((DMA_2->DMA_IFCR), 10);
		CLR_BIT((DMA_2->DMA_IFCR), 11);
		DMA2_CallBack[2]();
	}
	else {

	}
}
void DMA2_Channel4IRQHandler(void){
	if (DMA2_CallBack[3] != NULL_PTR){
		CLR_BIT((DMA_2->DMA_IFCR), 12);
		CLR_BIT((DMA_2->DMA_IFCR), 13);
		CLR_BIT((DMA_2->DMA_IFCR), 14);
		CLR_BIT((DMA_2->DMA_IFCR), 15);
		DMA2_CallBack[3]();
	}
	else {

	}

}
void DMA2_Channel5_IRQHandler(void){
	if (DMA2_CallBack[4] != NULL_PTR){
		CLR_BIT((DMA_2->DMA_IFCR), 16);
		CLR_BIT((DMA_2->DMA_IFCR), 17);
		CLR_BIT((DMA_2->DMA_IFCR), 18);
		CLR_BIT((DMA_2->DMA_IFCR), 19);
		DMA2_CallBack[4]();
	}
	else {

	}
}

