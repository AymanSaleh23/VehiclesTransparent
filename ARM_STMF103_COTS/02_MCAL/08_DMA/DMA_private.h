/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:18 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/
#ifndef DMA_PRIVATE_H_
#define DMA_PRIVATE_H_

#define DMA_1_BASE_ADDRESS	0x40020000
#define DMA_2_BASE_ADDRESS	0x40020400

/*	For each channel x (1:7)	Just multiply by 4 to reach for the desired channel	*/
/*	General Interrupt Flag for DMA	*/
#define DMA_ISR_GIFx	0
/*	Transfer Complete Interrupt Flag for DMA	*/
#define DMA_ISR_TCIFx	1
/*	Half Transfer Interrupt Flag for DMA	*/
#define DMA_ISR_HTIFx	2
/*	Transfer Error Interrupt Flag for DMA	*/
#define DMA_ISR_TEIFx	3

/*	For each channel x (1:7)	Just multiply by 4 to reach for the desired channel	*/
/*	0: no effect you can directly write the value for fast operation 				*/
/*	General Interrupt Flag Clear for DMA	*/
#define DMA_IFCR_CGIFx	0
/*	Transfer Complete Interrupt Flag Clear for DMA	*/
#define DMA_IFCR_CTCIFx	1
/*	Half Transfer Interrupt Flag Clear for DMA	*/
#define DMA_IFCR_CHTIFx	2
/*	Transfer Error Interrupt Flag Clear for DMA	*/
#define DMA_IFCR_CTEIFx	3

typedef struct {
	volatile u32 Channel_EN		:1;
	volatile u32 Channel_TCIE	:1;
	volatile u32 Channel_HTIE	:1;
	volatile u32 Channel_TEIE	:1;
	volatile u32 Channel_DIR	:1;
	volatile u32 Channel_CIRC	:1;
	volatile u32 Channel_PINC	:1;
	volatile u32 Channel_MINC	:1;
	volatile u32 Channel_PSIZE	:2;
	volatile u32 Channel_MSIZE	:2;
	volatile u32 Channel_PL		:2;
	volatile u32 Channel_MEM2MEM:1;
	volatile u32 Reserved		:17;
}DMA_Channel_Config;


typedef	struct {
	volatile DMA_Channel_Config CCRx;
	volatile u32 DMA_CNDTR;
	volatile u32 DMA_CPAR;
	volatile u32 DMA_CMAR;
	volatile u32 Reserved;
}DMA_Channel_t;

/*	DMA Channel	Struct	*/
typedef	struct {
	volatile u32 DMA_ISR;
	volatile u32 DMA_IFCR;
	volatile DMA_Channel_t Channel [7];

}DMA_t;

#define DMA_1	((volatile DMA_t * ) (DMA_1_BASE_ADDRESS + 0x00000000))
#define DMA_2	((volatile DMA_t * ) (DMA_2_BASE_ADDRESS + 0x00000000))


#define ENABLE 	1
#define DISABLE	2

/*	Idicator For Pre Build	*/
#define VERY_HIGH	0b11
#define HIGH		0b10
#define MEDIUM		0b01
#define LOW			0b00

/*	Idicator For Pre Build	*/
#define MEMORY_SIZE_8_BIT	0b00
#define MEMORY_SIZE_16_BIT	0b01
#define MEMORY_SIZE_32_BIT	0b10

/*	Idicator For User Post Build	*/
#define PERIPHERAL_SIZE_8_BIT	0b00
#define PERIPHERAL_SIZE_16_BIT	0b01
#define PERIPHERAL_SIZE_32_BIT	0b10


#define MEMROTY_INC_DISABLE	0
#define MEMROTY_INC_ENABLE	1

#define PERIPHERAL_INC_DISABLE	0
#define PERIPHERAL_INC_ENABLE	1

#define CIRCULAR_MODE_DISABLE	0
#define CIRCULAR_MODE_ENABLE	1

#define READ_FORM_MEMORY_ENABLE		1
#define READ_FORM_MEMORY_DISABLE	0

#define NULL_PTR 	((void *)0)

#define DMA_1_MAX_CHANNEL		7
#define DMA_2_MAX_CHANNEL		5

#endif
