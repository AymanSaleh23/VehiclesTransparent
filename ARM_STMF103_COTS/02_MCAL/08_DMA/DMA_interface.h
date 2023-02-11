/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:18 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/
#ifndef DMA_INTERFACE_H_
#define DMA_INTERFACE_H_

#define DMA_CHANNEL_1	1
#define DMA_CHANNEL_2	2
#define DMA_CHANNEL_3	3
#define DMA_CHANNEL_4	4
#define DMA_CHANNEL_5	5
#define DMA_CHANNEL_6	6
#define DMA_CHANNEL_7	7

/*	Idicator For User Post Build	*/
#define DMA_PRIORITY_VERY_HIGH	0b11
#define DMA_PRIORITY_HIGH		0b10
#define DMA_PRIORITY_MEDIUM		0b01
#define DMA_PRIORITY_LOW		0b00

/*	Idicator For User Post Build	*/
#define DMA_MEMORY_SIZE_8_BIT	0b00
#define DMA_MEMORY_SIZE_16_BIT	0b01
#define DMA_MEMORY_SIZE_32_BIT	0b10

/*	Idicator For User Post Build	*/
#define DMA_PERIPHERAL_SIZE_8_BIT	0b00
#define DMA_PERIPHERAL_SIZE_16_BIT	0b01
#define DMA_PERIPHERAL_SIZE_32_BIT	0b10

#define DMA_READ_FROM_MEMORY		1
#define DMA_READ_FROM_PERIPHERAL	0

#define DMA_MEMROTY_INC_DISABLE	0
#define DMA_MEMROTY_INC_ENABLE	1

#define DMA_PERIPHERAL_INC_DISABLE	0
#define DMA_PERIPHERAL_INC_ENABLE	1

#define DMA_CIRCULAR_MODE_DISABLE	0
#define DMA_CIRCULAR_MODE_ENABLE	1

#define DMA_GIF		0
#define DMA_TCIF	1
#define DMA_HTIF	2
#define DMA_TEIF	3

#define DMA_MODULE_1	1
#define DMA_MODULE_2	2

typedef struct{
	u8	DMA_module;
	u8	Channel;
	u8	Direction;
	u8	Priority;
	u8	MemoryInc;
	u8	PeripheralInc;
	u8	CircularOperation;
	u16	PeripheralSize;
	u16	MemorySize;
	u16	BlockLenght;
	u32	* pu32SourceAddress;
	u32	* pu32DestinationAddress;
	void (* fptr)(void);
}DMA_ChannelReq_t;

void 	MDMA_voidChannelInit			(void);
void	MDMA_voidChannelStartRequest	( DMA_ChannelReq_t * Copy_DMAReq);
void 	MDMA_voidChannelNewOrder		( DMA_ChannelReq_t * Copy_DMAReq , u32 Copy_u32NewSource, u32 Copy_u32NewDestination );
u8		MDMA_u8GetFlag					( DMA_ChannelReq_t * Copy_DMAReq, u8 Copy_u8Flag);

#endif
