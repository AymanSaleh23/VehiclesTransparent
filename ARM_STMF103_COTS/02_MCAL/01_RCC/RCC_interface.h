/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:6 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef _RCC_INTERFACE_H_
/*	define this file  */
#define _RCC_INTERFACE_H_

/*	Buses Types	*/
#define RCC_AHB		0
#define RCC_APB1	1
#define RCC_APB2	2

/*	Peripheral Enable For AHB Bus*/
#define RCC_AHB_DMA1EN	0
#define RCC_AHB_DMA2EN	1
#define RCC_AHB_SRAMEN	2
#define RCC_AHB_FLITFEN	4
#define RCC_AHB_CRCEN	6
#define RCC_AHB_FSMCEN	8
#define RCC_AHB_SDIOEN	10

/*	Peripheral Enable For APB1 Bus*/
#define RCC_APB1_TIM2EN		0
#define RCC_APB1_TIM3EN		1
#define RCC_APB1_TIM4EN		2
#define RCC_APB1_TIM5EN		3
#define RCC_APB1_TIM6EN		4
#define RCC_APB1_TIM7EN		5
#define RCC_APB1_TIM12EN		6
#define RCC_APB1_TIM13EN		7
#define RCC_APB1_TIM14EN		8
#define RCC_APB1_WWDGEN		11
#define RCC_APB1_SPI2EN		14
#define RCC_APB1_SPI3EN		15
#define RCC_APB1_USART2EN	17
#define RCC_APB1_USART3EN	18
#define RCC_APB1_USART4EN	19
#define RCC_APB1_USART5EN	20
#define RCC_APB1_I2C1EN		21
#define RCC_APB1_I2C2EN		22
#define RCC_APB1_USBEN		23
#define RCC_APB1_CANEN		25
#define RCC_APB1_BKPEN		27
#define RCC_APB1_PWREN		28
#define RCC_APB1_DACEN		29

/*	Peripheral Enable For APB2 Bus*/
#define RCC_APB2_AFIOEN		0
#define RCC_APB2_IOPAEN		2
#define RCC_APB2_IOPBEN		3
#define RCC_APB2_IOPCEN		4
#define RCC_APB2_IOPDEN		5
#define RCC_APB2_IOPEEN		6
#define RCC_APB2_IOPFEN		7
#define RCC_APB2_IOPGEN		8
#define RCC_APB2_ADC1EN		9
#define RCC_APB2_ADC2EN		10
#define RCC_APB2_TIM1EN		11
#define RCC_APB2_SPI1EN		12
#define RCC_APB2_TIM8EN		13
#define RCC_APB2_USART1EN	14
#define RCC_APB2_ADC3EN		15
#define RCC_APB2_TIM9EN		19
#define RCC_APB2_TIM10EN	20
#define RCC_APB2_TIM11EN	21


void RCC_voidInitSysClock (void);
void RCC_voidEnableClock ( u8 Copy_u8BusId, u8 Copy_u8PreId );
void RCC_voidDisableClock ( u8 Copy_u8BusId, u8 Copy_u8PreId );
/*	end of Preprocessor directive */
#endif
