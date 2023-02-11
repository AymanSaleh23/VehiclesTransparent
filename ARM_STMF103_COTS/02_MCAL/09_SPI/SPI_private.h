
/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:20 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/


#ifndef SPI_PRIVATE_H_
#define SPI_PRIVATE_H_

typedef struct{
	volatile u32 CR1;
	volatile u32 CR2;
	volatile u32 SR;
	volatile u32 DR;
	volatile u32 CRCPR;
	volatile u32 RXCRC;
	volatile u32 TXCRC;
	volatile u32 I2SCFGR;
	volatile u32 I2SPR;

}SPI_register;

#define SPI1_BASE_ADDRESS	(0x40013000)
#define SPI2_BASE_ADDRESS   (0x40003800)
#define SPI3_BASE_ADDRESS   (0x40003C00)

#define SPI1_REGISTER		((SPI_register *)(SPI1_BASE_ADDRESS +0x00000000))
#define SPI2_REGISTER		((SPI_register *)(SPI2_BASE_ADDRESS +0x00000000))
#define SPI3_REGISTER		((SPI_register *)(SPI3_BASE_ADDRESS +0x00000000))

#define SPI_CR1_CPHA		0
#define SPI_CR1_CPOL		1
#define SPI_CR1_MSTR		2
#define SPI_CR1_SPE			6
#define SPI_CR1_LBSFIRST	7
#define SPI_CR1_SSI			8
#define SPI_CR1_SSM			9
#define SPI_CR1_RXONLY		10
#define SPI_CR1_DFF			11
#define SPI_CR1_CRCNEXT		12
#define SPI_CR1_CRCEN		13
#define SPI_CR1_BIDIOE		14
#define SPI_CR1_BIDIMODE	15

#define SPI_SR_RXNE		0
#define SPI_SR_TXE		1
#define SPI_SR_CHSIDE	2
#define SPI_SR_UDR		3
#define SPI_SR_CRCERR	4
#define SPI_SR_MODEF	5
#define SPI_SR_OVR		6
#define SPI_SR_BSY		7

#define SPI_CR2_RXDMAEN			0
#define SPI_CR2_TXDMAEN			1
#define SPI_CR2_SSOE			2
#define SPI_CR2_ERRIE			5
#define SPI_CR2_RXNEIE			6
#define SPI_CR2_TXEIE			7

#define SPI_SR_RXNE		0
#define SPI_SR_TXE		1
#define SPI_SR_CHSDIE	2
#define SPI_SR_UDR		3
#define SPI_SR_CRCERR	4
#define SPI_SR_MODF		5
#define SPI_SR_OVR		6
#define SPI_SR_BSY		7

#define SPI_I2SCFGR I2SMOD 		7
#define SPI_I2SCFGR I2SE 		6
#define SPI_I2SCFGR I2SCFG 		5
#define SPI_I2SCFGR PCMSYNC		4
#define SPI_I2SCFGR I2SSTD 		3
#define SPI_I2SCFGR CKPOL 		2
#define SPI_I2SCFGR DATLEN 		1
#define SPI_I2SCFGR CHLEN		0

#define ENABLE				1
#define DISABLE				0

#define MASTER				1
#define SLAVE 				0

#define IDLE_LOW 			0
#define IDLE_HIGH			1

#define SECOND_EDGE			1
#define FIRST_EDGE 			0

#define SPI_CR1_BR_MASK			0xFFC7

#define BR_DIV_BY_2		0b000
#define BR_DIV_BY_4		0b001
#define BR_DIV_BY_8   	0b010
#define BR_DIV_BY_16  	0b011
#define BR_DIV_BY_32  	0b100
#define BR_DIV_BY_64  	0b101
#define BR_DIV_BY_182 	0b110
#define BR_DIV_BY_256 	0b111

#define LSB_FIRST		1
#define MSB_FIRST		0

#define FRAME_8_BIT 			0
#define FRAME_16_BIT			1

#define RESET_NOT_STD_CONFIG	0x00FF
#define NULL_PTR		(void*)0
#endif
