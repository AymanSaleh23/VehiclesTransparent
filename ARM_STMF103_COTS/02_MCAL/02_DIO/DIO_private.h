/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:10 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef DIO_PRIVATE_H_
#define DIO_PRIVATE_H_
/*	GPIO Ports Base Addresses*/
#define GPIOA_BASE_ADDRESS (0x40010800)
#define GPIOB_BASE_ADDRESS (0x40010C00)
#define GPIOC_BASE_ADDRESS (0x40011000)
#define GPIOD_BASE_ADDRESS (0x40011400)
#define GPIOE_BASE_ADDRESS (0x40011800)
#define GPIOF_BASE_ADDRESS (0x40011C00)
#define GPIOG_BASE_ADDRESS (0x40012000)

/*	GPIO PORT A Registers Definition	*/
#define GPIOA_CRL	*((u32*)(GPIOA_BASE_ADDRESS+0x00) )
#define GPIOA_CRH	*((u32*)(GPIOA_BASE_ADDRESS+0x04) )
#define GPIOA_IDR	*((u32*)(GPIOA_BASE_ADDRESS+0x08) )
#define GPIOA_ODR	*((u32*)(GPIOA_BASE_ADDRESS+0x0C) )
#define GPIOA_BSR	*((u32*)(GPIOA_BASE_ADDRESS+0x10) )
#define GPIOA_BRR	*((u32*)(GPIOA_BASE_ADDRESS+0x14) )
#define GPIOA_LCK	*((u32*)(GPIOA_BASE_ADDRESS+0x18) )

/*	GPIO PORT B Registers Definition	*/
#define GPIOB_CRL	*((u32*)(GPIOB_BASE_ADDRESS+0x00) )
#define GPIOB_CRH	*((u32*)(GPIOB_BASE_ADDRESS+0x04) )
#define GPIOB_IDR	*((u32*)(GPIOB_BASE_ADDRESS+0x08) )
#define GPIOB_ODR	*((u32*)(GPIOB_BASE_ADDRESS+0x0C) )
#define GPIOB_BSR	*((u32*)(GPIOB_BASE_ADDRESS+0x10) )
#define GPIOB_BRR	*((u32*)(GPIOB_BASE_ADDRESS+0x14) )
#define GPIOB_LCK	*((u32*)(GPIOB_BASE_ADDRESS+0x18) )

/*	GPIO PORT C Registers Definition	*/
#define GPIOC_CRL	*((u32*)(GPIOC_BASE_ADDRESS+0x00) )
#define GPIOC_CRH	*((u32*)(GPIOC_BASE_ADDRESS+0x04) )
#define GPIOC_IDR	*((u32*)(GPIOC_BASE_ADDRESS+0x08) )
#define GPIOC_ODR	*((u32*)(GPIOC_BASE_ADDRESS+0x0C) )
#define GPIOC_BSR	*((u32*)(GPIOC_BASE_ADDRESS+0x10) )
#define GPIOC_BRR	*((u32*)(GPIOC_BASE_ADDRESS+0x14) )
#define GPIOC_LCK	*((u32*)(GPIOC_BASE_ADDRESS+0x18) )

/*	GPIO PORT D Registers Definition	*/
#define GPIOD_CRL	*((u32*)(GPIOD_BASE_ADDRESS+0x00) )
#define GPIOD_CRH	*((u32*)(GPIOD_BASE_ADDRESS+0x04) )
#define GPIOD_IDR	*((u32*)(GPIOD_BASE_ADDRESS+0x08) )
#define GPIOD_ODR	*((u32*)(GPIOD_BASE_ADDRESS+0x0C) )
#define GPIOD_BSR	*((u32*)(GPIOD_BASE_ADDRESS+0x10) )
#define GPIOD_BRR	*((u32*)(GPIOD_BASE_ADDRESS+0x14) )
#define GPIOD_LCK	*((u32*)(GPIOD_BASE_ADDRESS+0x18) )

/*	GPIO PORT E Registers Definition	*/
#define GPIOE_CRL	*((u32*)(GPIOE_BASE_ADDRESS+0x00) )
#define GPIOE_CRH	*((u32*)(GPIOE_BASE_ADDRESS+0x04) )
#define GPIOE_IDR	*((u32*)(GPIOE_BASE_ADDRESS+0x08) )
#define GPIOE_ODR	*((u32*)(GPIOE_BASE_ADDRESS+0x0C) )
#define GPIOE_BSR	*((u32*)(GPIOE_BASE_ADDRESS+0x10) )
#define GPIOE_BRR	*((u32*)(GPIOE_BASE_ADDRESS+0x14) )
#define GPIOE_LCK	*((u32*)(GPIOE_BASE_ADDRESS+0x18) )

/*	GPIO PORT F Registers Definition	*/
#define GPIOF_CRL	*((u32*)(GPIOF_BASE_ADDRESS+0x00) )
#define GPIOF_CRH	*((u32*)(GPIOF_BASE_ADDRESS+0x04) )
#define GPIOF_IDR	*((u32*)(GPIOF_BASE_ADDRESS+0x08) )
#define GPIOF_ODR	*((u32*)(GPIOF_BASE_ADDRESS+0x0C) )
#define GPIOF_BSR	*((u32*)(GPIOF_BASE_ADDRESS+0x10) )
#define GPIOF_BRR	*((u32*)(GPIOF_BASE_ADDRESS+0x14) )
#define GPIOF_LCK	*((u32*)(GPIOF_BASE_ADDRESS+0x18) )

/*	GPIO PORT G Registers Definition	*/
#define GPIOG_CRL	*((u32*)(GPIOG_BASE_ADDRESS+0x00) )
#define GPIOG_CRH	*((u32*)(GPIOG_BASE_ADDRESS+0x04) )
#define GPIOG_IDR	*((u32*)(GPIOG_BASE_ADDRESS+0x08) )
#define GPIOG_ODR	*((u32*)(GPIOG_BASE_ADDRESS+0x0C) )
#define GPIOG_BSR	*((u32*)(GPIOG_BASE_ADDRESS+0x10) )
#define GPIOG_BRR	*((u32*)(GPIOG_BASE_ADDRESS+0x14) )
#define GPIOG_LCK	*((u32*)(GPIOG_BASE_ADDRESS+0x18) )

#define DIO_MODE_CONFIG_MASK	0b1111

#endif
