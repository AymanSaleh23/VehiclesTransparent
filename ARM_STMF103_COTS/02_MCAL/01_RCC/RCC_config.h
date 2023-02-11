/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:6 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef _RCC_CONFIG_H_
/*	define this file  */
#define _RCC_CONFIG_H_

/*	Options:	RCC_HSE_CRYSTAL
				RCC_HSE_RC
				RCC_HSI
				RCC_PLL
*/
#define FCC_CLOCK_TYPE	RCC_HSI


#if FCC_CLOCK_TYPE == RCC_PLL
/*	Options 	RCC_PLL_IN_HSI_DIV_2
				RCC_PLL_IN_HSE_DIV_2
				RCC_PLL_IN_HSE
*/
/*Note: Select Value only if RCC_PLL is selected*/
#define RCC_PLL_INPUT	RCC_PLL_IN_HSE
/*	Options: 2 to 16*/
/*Note: Select Value only if RCC_PLL is selected*/
/*Caution: The PLL output frequency must not exceed 72 MHz*/
#define RCC_PLL_MUL_VAL		4
#endif 
/*	Options 	RCC_MCO_NO_CLK
				RCC_MCO_SYS_CLK
				RCC_MCO_HSI
				RCC_MCO_HSE
				RCC_MCO_PLL_DIV_2
*/
#define FCC_MCO_OUT		RCC_MCO_SYS_CLK
/*	end of Preprocessor directive */
#endif
