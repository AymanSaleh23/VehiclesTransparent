
/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:20 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#ifndef SPI_CONFIG_H_
#define SPI_CONFIG_H_

/*
 * 		Note:
 * 			By Default
 * 			DMA with SPI, SSI, Bidirectional, CRC
 * 			are Disabled for all SPI channels
 */

/**************	SPI1 Configurations	********************/
/*	Options:
 * 		ENABLE
 * 		DISABLE
 */
#define SPI1_STATE	ENABLE


/*	Write in Pairs GPIO_PORTx, GPIO_PINx
 */
#define SPI1_SLAVE_PIN 	GPIO_PORTA, GPIO_PIN0


/*	Options:
 * 		MASTER
 * 		SLAVE
 */
#define SPI1_MODE	MASTER
/*	Options:
 * 		IDLE_LOW
 * 		IDLE_HIGH
 */
#define SPI1_CLK_IDLE	IDLE_HIGH

/*	Options:
 * 		SECOND_EDGE
 * 		FIRST_EDGE
 */
#define SPI1_READING_EDGE	SECOND_EDGE

/*	Options:
 * 		BR_DIV_BY_2
 * 		BR_DIV_BY_4
 * 		BR_DIV_BY_8
 * 		BR_DIV_BY_16
 * 		BR_DIV_BY_32
 * 		BR_DIV_BY_64
 * 		BR_DIV_BY_182
 * 		BR_DIV_BY_256
 */
#define SPI1_BAUDRATE	BR_DIV_BY_2

/*	Options:
 * 		LSB_FIRST
 * 		MSB_FIRST
 */
#define SPI1_FIRST_BIT	MSB_FIRST

/*	Options:
 * 		FRAME_8_BIT
 * 		FRAME_16_BIT
 */
#define SPI1_FRAME_FORMAT	FRAME_8_BIT

/**************	SPI2 Configurations	********************/
/*	Options:
 * 		ENABLE
 * 		DISABLE
 */
#define SPI2_STATE	ENABLE


/*	Write in Pairs GPIO_PORTx, GPIO_PINx
 */
#define SPI2_SLAVE_PIN 	GPIO_PORTA, GPIO_PIN1


/*	Options:
 * 		MASTER
 * 		SLAVE
 */
#define SPI2_MODE	SLAVE
/*	Options:
 * 		IDLE_LOW
 * 		IDLE_HIGH
 */
#define SPI2_CLK_IDLE	IDLE_HIGH

/*	Options:
 * 		SECOND_EDGE
 * 		FIRST_EDGE
 */
#define SPI2_READING_EDGE	SECOND_EDGE

/*	Options:
 * 		BR_DIV_BY_2
 * 		BR_DIV_BY_4
 * 		BR_DIV_BY_8
 * 		BR_DIV_BY_16
 * 		BR_DIV_BY_32
 * 		BR_DIV_BY_64
 * 		BR_DIV_BY_182
 * 		BR_DIV_BY_256
 */
#define SPI2_BAUDRATE	BR_DIV_BY_64

/*	Options:
 * 		LSB_FIRST
 * 		MSB_FIRST
 */
#define SPI2_FIRST_BIT	LSB_FIRST

/*	Options:
 * 		FRAME_8_BIT
 * 		FRAME_16_BIT
 */
#define SPI2_FRAME_FORMAT	FRAME_8_BIT

/**************	SPI3 Configurations	********************/
/*	Options:
 * 		ENABLE
 * 		DISABLE
 */
#define SPI3_STATE	DISABLE


/*	Write in Pairs GPIO_PORTx, GPIO_PINx
 */
#define SPI3_SLAVE_PIN 	GPIO_PORTA, GPIO_PIN2


/*	Options:
 * 		MASTER
 * 		SLAVE
 */
#define SPI3_MODE	MASTER
/*	Options:
 * 		IDLE_LOW
 * 		IDLE_HIGH
 */
#define SPI3_CLK_IDLE	IDLE_HIGH

/*	Options:
 * 		SECOND_EDGE
 * 		FIRST_EDGE
 */
#define SPI3_READING_EDGE	SECOND_EDGE

/*	Options:
 * 		BR_DIV_BY_2
 * 		BR_DIV_BY_4
 * 		BR_DIV_BY_8
 * 		BR_DIV_BY_16
 * 		BR_DIV_BY_32
 * 		BR_DIV_BY_64
 * 		BR_DIV_BY_182
 * 		BR_DIV_BY_256
 */
#define SPI3_BAUDRATE	BR_DIV_BY_64

/*	Options:
 * 		LSB_FIRST
 * 		MSB_FIRST
 */
#define SPI3_FIRST_BIT	LSB_FIRST

/*	Options:
 * 		FRAME_8_BIT
 * 		FRAME_16_BIT
 */
#define SPI3_FRAME_FORMAT	FRAME_8_BIT
#endif
