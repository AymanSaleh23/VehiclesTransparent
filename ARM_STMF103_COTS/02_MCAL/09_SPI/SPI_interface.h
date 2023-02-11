
/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:20 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/
#ifndef SPI_INTERFACE_H_
#define SPI_INTERFACE_H_

#define SPI1_MODULE		1
#define SPI2_MODULE		2
#define SPI3_MODULE		3

#define SPI_ENABLE		1
#define SPI_DISABLE		0

#define SPI_MASTER		1
#define SPI_SLAVE		0

#define SPI_CLK_IDLE_LOW		0
#define SPI_CLK_IDLE_HIGH		1

#define SPI_READ_SECOND_EDGE	1
#define SPI_READ_FIRST_EDGE		0

#define SPI_BR_DIV_BY_2			0
#define SPI_BR_DIV_BY_4			1
#define SPI_BR_DIV_BY_8			2
#define SPI_BR_DIV_BY_16		3
#define SPI_BR_DIV_BY_32		4
#define SPI_BR_DIV_BY_64		5
#define SPI_BR_DIV_BY_182		6
#define SPI_BR_DIV_BY_256		7

#define SPI_LSB_FIRST			1
#define SPI_MSB_FIRST			0

#define SPI_FRAME_8_BIT		0
#define SPI_FRAME_16_BIT	1


void MSPI1_voidInit (void);
void MSPI1_voidSendReceiveSynch(u16 Copy_u16DataToSend, u16 * Copy_u16DataToReceive);
/*	The call back function take the address of variable to hold the received data	*/
void MSPI1_voidSendReceiveAsynch(u16 Copy_u16DataToSend, void (*callBack)(u16));

void MSPI2_voidInit (void);
void MSPI2_voidSendReceiveSynch(u16 Copy_u16DataToSend, u16 * Copy_u16DataToReceive);
/*	The call back function take the address of variable to hold the received data	*/
void MSPI2_voidSendReceiveAsynch(u16 Copy_u16DataToSend, void (*callBack)(u16));

void MSPI3_voidInit (void);
void MSPI3_voidSendReceiveSynch(u16 Copy_u16DataToSend, u16 * Copy_u16DataToReceive);
/*	The call back function take the address of variable to hold the received data	*/
void MSPI3_voidSendReceiveAsynch(u16 Copy_u16DataToSend, void (*callBack)(u16));

#endif
