
/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:20 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/


#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "DIO_interface.h"

#include "SPI_interface.h"
#include "SPI_private.h"
#include "SPI_config.h"

void (*SPI_callBack[3])(u16)= {NULL_PTR};

void MSPI1_voidInit (void){
	/*	SPI1_STATE	Start	*/
#if 	SPI1_STATE	==	ENABLE
	/*0b0000 1111 1111 1111*/
	SPI1_REGISTER->CR1 	&= RESET_NOT_STD_CONFIG;

	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_SSI);
	/*	SPI1_BAUDRATE	Start	*/
#if		SPI1_BAUDRATE	>=	BR_DIV_BY_2 && 	SPI1_BAUDRATE	<= BR_DIV_BY_256
	SPI1_REGISTER->CR1 &= SPI_CR1_BR_MASK;
	SPI1_REGISTER->CR1 = (SPI1_REGISTER->CR1 | (SPI1_BAUDRATE<<3)) ;
#else
#error	"Wrong SPI1_BAUDRATE configuration parameter"
	/*	SPI1_BAUDRATE	End	*/
#endif


	/*	SPI1_CLK_IDLE	Start	*/
#if		SPI1_CLK_IDLE	==	IDLE_LOW
	CLR_BIT(SPI1_REGISTER->CR1, SPI_CR1_CPOL);
#elif	SPI1_CLK_IDLE	==	IDLE_HIGH
	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_CPOL);
#else
#error	"Wrong SPI1_CLK_IDLE configuration parameter"
	/*	SPI1_CLK_IDLE	End	*/
#endif
	/*	SPI1_READING_EDGE	Start	*/
#if		SPI1_READING_EDGE	==	SECOND_EDGE
	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_CPHA);
#elif	SPI1_READING_EDGE	==	FIRST_EDGE
#warning	"Not Recommended SPI1_READING_EDGE configuration parameter to be FIRST_EDGE"
	CLR_BIT(SPI1_REGISTER->CR1, SPI_CR1_CPHA);
#else
#error	"Wrong SPI1_READING_EDGE configuration parameter"
	/*	SPI1_READING_EDGE	End	*/
#endif

	/*	SPI1_FRAME_FORMAT	Start	*/
#if		SPI1_FRAME_FORMAT	==	FRAME_8_BIT
	CLR_BIT(SPI1_REGISTER->CR1, SPI_CR1_DFF);
#elif	SPI1_FRAME_FORMAT	==	FRAME_16_BIT
	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_DFF);
#else
#error	"Wrong SPI1_FRAME_FORMAT configuration parameter"
	/*	SPI1_FRAME_FORMAT	End		*/
#endif

	/*	SPI1_FIRST_BIT	Start	*/
#if		SPI1_FIRST_BIT	==	LSB_FIRST
	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_LBSFIRST);
#elif	SPI1_FIRST_BIT	==	MSB_FIRST
	CLR_BIT(SPI1_REGISTER->CR1, SPI_CR1_LBSFIRST);
#else
#error	"Wrong SPI1_FIRST_BIT configuration parameter"
	/*	SPI1_FIRST_BIT	End		*/
#endif

	/*	SPI1_MODE	Start	*/
#if		SPI1_MODE	==	MASTER
	/*	Enable SSM -Physical NSS pin will be disconnected from SPI-	*/
	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_SSM);
	/*	Put NSS to High by Software using SSI	*/
	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_MSTR);
#elif	SPI1_MODE	==	SLAVE
	CLR_BIT(SPI1_REGISTER->CR1, SPI_CR1_MSTR);
#else
#error	"Wrong SPI1_MODE configuration parameter"
	/*	SPI1_MODE	End	*/
#endif

	SET_BIT(SPI1_REGISTER->CR1, SPI_CR1_SPE);

#elif 	SPI1_STATE	==	DISABLE
	CLR_BIT(SPI1_REGISTER->CR1, SPI_CR1_SPE);
#else
#error	"Wrong SPI1_STATE configuration parameter"
	/*	SPI1_STATE	End	*/
#endif
}
void MSPI2_voidInit (void){
	/*	SPI2_STATE	Start	*/
#if 	SPI2_STATE	==	ENABLE
	/*0b0000 1111 1111 1111*/
	SPI2_REGISTER->CR1 	&= RESET_NOT_STD_CONFIG;

	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_SSI);
	/*	SPI2_BAUDRATE	Start	*/
#if		SPI2_BAUDRATE	>=	BR_DIV_BY_2 && 	SPI2_BAUDRATE	<= BR_DIV_BY_256
	SPI2_REGISTER->CR1 &= SPI_CR1_BR_MASK;
	SPI2_REGISTER->CR1 = (SPI2_REGISTER->CR1 | (SPI2_BAUDRATE<<3)) ;
#else
#error	"Wrong SPI2_BAUDRATE configuration parameter"
	/*	SPI2_BAUDRATE	End	*/
#endif


	/*	SPI2_CLK_IDLE	Start	*/
#if		SPI2_CLK_IDLE	==	IDLE_LOW
	CLR_BIT(SPI2_REGISTER->CR1, SPI_CR1_CPOL);
#elif	SPI2_CLK_IDLE	==	IDLE_HIGH
	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_CPOL);
#else
#error	"Wrong SPI2_CLK_IDLE configuration parameter"
	/*	SPI2_CLK_IDLE	End	*/
#endif
	/*	SPI2_READING_EDGE	Start	*/
#if		SPI2_READING_EDGE	==	SECOND_EDGE
	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_CPHA);
#elif	SPI2_READING_EDGE	==	FIRST_EDGE
#warning	"Not Recommended SPI2_READING_EDGE configuration parameter to be FIRST_EDGE"
	CLR_BIT(SPI2_REGISTER->CR1, SPI_CR1_CPHA);
#else
#error	"Wrong SPI2_READING_EDGE configuration parameter"
	/*	SPI2_READING_EDGE	End	*/
#endif

	/*	SPI2_FRAME_FORMAT	Start	*/
#if		SPI2_FRAME_FORMAT	==	FRAME_8_BIT
	CLR_BIT(SPI2_REGISTER->CR1, SPI_CR1_DFF);
#elif	SPI2_FRAME_FORMAT	==	FRAME_16_BIT
	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_DFF);
#else
#error	"Wrong SPI2_FRAME_FORMAT configuration parameter"
	/*	SPI2_FRAME_FORMAT	End		*/
#endif

	/*	SPI2_FIRST_BIT	Start	*/
#if		SPI2_FIRST_BIT	==	LSB_FIRST
	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_LBSFIRST);
#elif	SPI2_FIRST_BIT	==	MSB_FIRST
	CLR_BIT(SPI2_REGISTER->CR1, SPI_CR1_LBSFIRST);
#else
#error	"Wrong SPI2_FIRST_BIT configuration parameter"
	/*	SPI2_FIRST_BIT	End		*/
#endif

	/*	SPI2_MODE	Start	*/
#if		SPI2_MODE	==	MASTER
	/*	Enable SSM -Physical NSS pin will be disconnected from SPI-	*/
	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_SSM);
	/*	Put NSS to High by Software using SSI	*/
	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_MSTR);
#elif	SPI2_MODE	==	SLAVE
	CLR_BIT(SPI2_REGISTER->CR1, SPI_CR1_MSTR);
#else
#error	"Wrong SPI2_MODE configuration parameter"
	/*	SPI2_MODE	End	*/
#endif

	SET_BIT(SPI2_REGISTER->CR1, SPI_CR1_SPE);

#elif 	SPI2_STATE	==	DISABLE
	CLR_BIT(SPI2_REGISTER->CR1, SPI_CR1_SPE);
#else
#error	"Wrong SPI2_STATE configuration parameter"
	/*	SPI2_STATE	End	*/
#endif
}
void MSPI3_voidInit (void){
	/*	SPI3_STATE	Start	*/
#if 	SPI3_STATE	==	ENABLE
	/*0b0000 1111 1111 1111*/
	SPI3_REGISTER->CR1 	&= RESET_NOT_STD_CONFIG;

	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_SSI);
	/*	SPI3_BAUDRATE	Start	*/
#if		SPI3_BAUDRATE	>=	BR_DIV_BY_2 && 	SPI3_BAUDRATE	<= BR_DIV_BY_256
	SPI3_REGISTER->CR1 &= SPI_CR1_BR_MASK;
	SPI3_REGISTER->CR1 = (SPI3_REGISTER->CR1 | (SPI3_BAUDRATE<<3)) ;
#else
#error	"Wrong SPI3_BAUDRATE configuration parameter"
	/*	SPI3_BAUDRATE	End	*/
#endif


	/*	SPI3_CLK_IDLE	Start	*/
#if		SPI3_CLK_IDLE	==	IDLE_LOW
	CLR_BIT(SPI3_REGISTER->CR1, SPI_CR1_CPOL);
#elif	SPI3_CLK_IDLE	==	IDLE_HIGH
	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_CPOL);
#else
#error	"Wrong SPI3_CLK_IDLE configuration parameter"
	/*	SPI3_CLK_IDLE	End	*/
#endif
	/*	SPI3_READING_EDGE	Start	*/
#if		SPI3_READING_EDGE	==	SECOND_EDGE
	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_CPHA);
#elif	SPI3_READING_EDGE	==	FIRST_EDGE
#warning	"Not Recommended SPI3_READING_EDGE configuration parameter to be FIRST_EDGE"
	CLR_BIT(SPI3_REGISTER->CR1, SPI_CR1_CPHA);
#else
#error	"Wrong SPI3_READING_EDGE configuration parameter"
	/*	SPI3_READING_EDGE	End	*/
#endif

	/*	SPI3_FRAME_FORMAT	Start	*/
#if		SPI3_FRAME_FORMAT	==	FRAME_8_BIT
	CLR_BIT(SPI3_REGISTER->CR1, SPI_CR1_DFF);
#elif	SPI3_FRAME_FORMAT	==	FRAME_16_BIT
	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_DFF);
#else
#error	"Wrong SPI3_FRAME_FORMAT configuration parameter"
	/*	SPI3_FRAME_FORMAT	End		*/
#endif

	/*	SPI3_FIRST_BIT	Start	*/
#if		SPI3_FIRST_BIT	==	LSB_FIRST
	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_LBSFIRST);
#elif	SPI3_FIRST_BIT	==	MSB_FIRST
	CLR_BIT(SPI3_REGISTER->CR1, SPI_CR1_LBSFIRST);
#else
#error	"Wrong SPI3_FIRST_BIT configuration parameter"
	/*	SPI3_FIRST_BIT	End		*/
#endif

	/*	SPI3_MODE	Start	*/
#if		SPI3_MODE	==	MASTER
	/*	Enable SSM -Physical NSS pin will be disconnected from SPI-	*/
	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_SSM);
	/*	Put NSS to High by Software using SSI	*/
	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_MSTR);
#elif	SPI3_MODE	==	SLAVE
	CLR_BIT(SPI3_REGISTER->CR1, SPI_CR1_MSTR);
#else
#error	"Wrong SPI3_MODE configuration parameter"
	/*	SPI3_MODE	End	*/
#endif

	SET_BIT(SPI3_REGISTER->CR1, SPI_CR1_SPE);

#elif 	SPI3_STATE	==	DISABLE
	CLR_BIT(SPI3_REGISTER->CR1, SPI_CR1_SPE);
#else
#error	"Wrong SPI3_STATE configuration parameter"
	/*	SPI3_STATE	End	*/
#endif
}

void MSPI1_voidSendReceiveSynch(u16 Copy_u16DataToSend, u16 * Copy_u16DataToReceive){
	/*	Enable Slave	*/
	DIO_voidSetPinValue(SPI1_SLAVE_PIN 	, GPIO_PIN_LOW);
	SPI1_REGISTER->DR = (u8)Copy_u16DataToSend;
	/*	Wait for the Busy flag	*/
	while (GET_BIT(SPI1_REGISTER->SR, SPI_SR_BSY) == 1);
	/*	Return to the received data	*/
	*Copy_u16DataToReceive = SPI1_REGISTER->DR;

	/*	Disable Slave	*/
	DIO_voidSetPinValue(SPI1_SLAVE_PIN 	, GPIO_PIN_HIGH);

}
void MSPI2_voidSendReceiveSynch(u16 Copy_u16DataToSend, u16 * Copy_u16DataToReceive){
	/*	Enable Slave	*/
	DIO_voidSetPinValue(SPI2_SLAVE_PIN 	, GPIO_PIN_LOW);
	SPI2_REGISTER->DR = Copy_u16DataToSend;
	/*	Wait for the Busy flag	*/
	while (GET_BIT(SPI2_REGISTER->SR, SPI_SR_BSY) == 1);

	/*	Return to the received data	*/
	*Copy_u16DataToReceive = SPI2_REGISTER->DR;
	/*	Disable Slave	*/
	DIO_voidSetPinValue(SPI2_SLAVE_PIN 	, GPIO_PIN_HIGH);

}
void MSPI3_voidSendReceiveSynch(u16 Copy_u16DataToSend, u16 * Copy_u16DataToReceive){
	/*	Enable Slave	*/
	DIO_voidSetPinValue(SPI3_SLAVE_PIN 	, GPIO_PIN_LOW);
	SPI3_REGISTER->DR = Copy_u16DataToSend;
	/*	Wait for the Busy flag	*/
	while (GET_BIT(SPI3_REGISTER->SR, SPI_SR_BSY) == 1);

	/*	Return to the received data	*/
	*Copy_u16DataToReceive = SPI3_REGISTER->DR;
	/*	Disable Slave	*/
	DIO_voidSetPinValue(SPI3_SLAVE_PIN 	, GPIO_PIN_HIGH);

}


void MSPI1_voidSendReceiveAsynch(u16 Copy_u16DataToSend, void (*callBack)(u16)){
	if (callBack != NULL_PTR){
		SET_BIT(SPI1_REGISTER->CR2,SPI_CR2_TXEIE);
		SET_BIT(SPI1_REGISTER->CR2,SPI_CR2_RXNEIE);
		SPI_callBack[0] = callBack;
	}
}
void MSPI2_voidSendReceiveAsynch(u16 Copy_u16DataToSend, void (*callBack)(u16)){
	if (callBack != NULL_PTR){
		SET_BIT(SPI2_REGISTER->CR2,SPI_CR2_TXEIE);
		SET_BIT(SPI2_REGISTER->CR2,SPI_CR2_RXNEIE);
		SPI_callBack[1] = callBack;
	}
}
void MSPI3_voidSendReceiveAsynch(u16 Copy_u16DataToSend, void (*callBack)(u16)){
	if (callBack != NULL_PTR){
		SET_BIT(SPI3_REGISTER->CR2,SPI_CR2_TXEIE);
		SET_BIT(SPI3_REGISTER->CR2,SPI_CR2_RXNEIE);
		SPI_callBack[2] = callBack;
	}
}

void MSPI_voidDisable(u8 Copy_u8SPIModule){
	switch (Copy_u8SPIModule){
	case SPI1_MODULE:{
		while 	( GET_BIT(SPI1_REGISTER->SR, SPI_SR_RXNE) == 1);
		while 	( GET_BIT(SPI1_REGISTER->SR, SPI_SR_BSY ) == 1);
		CLR_BIT( 		  SPI1_REGISTER->CR1,SPI_CR1_SPE);
	}break;
	case SPI2_MODULE:{
		while 	( GET_BIT(SPI2_REGISTER->SR, SPI_SR_RXNE) == 1);
		while 	( GET_BIT(SPI2_REGISTER->SR, SPI_SR_BSY ) == 1);
		CLR_BIT( 		  SPI2_REGISTER->CR1,SPI_CR1_SPE);
	}break;
	case SPI3_MODULE:{
		while 	( GET_BIT(SPI3_REGISTER->SR, SPI_SR_RXNE) == 1);
		while 	( GET_BIT(SPI3_REGISTER->SR, SPI_SR_BSY ) == 1);
		CLR_BIT( 		  SPI3_REGISTER->CR1,SPI_CR1_SPE);
	}break;
	}
}

void SPI1_IRQHandler(void){
	if (SPI_callBack[0] != NULL_PTR){
		SPI_callBack[0](SPI1_REGISTER->DR);
	}
}
void SPI2_IRQHandler(void){
	if (SPI_callBack[1] != NULL_PTR){
		SPI_callBack[1](SPI2_REGISTER->DR);
	}
}
void SPI3_IRQHandler(void){
	if (SPI_callBack[2] != NULL_PTR){
		SPI_callBack[2](SPI3_REGISTER->DR);
	}
}
