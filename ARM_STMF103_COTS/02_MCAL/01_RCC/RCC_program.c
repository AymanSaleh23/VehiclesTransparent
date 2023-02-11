/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:6 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "RCC_interface.h"
#include "RCC_private.h"
#include "RCC_config.h"


void RCC_voidInitSysClock (void){
	/*Validate input configurations*/

	/* FCC_CLOCK_TYPE configuration parameter Check start*/
#if 	FCC_CLOCK_TYPE 	==	RCC_HSE_CRYSTAL
	//0x00010000
	/*	Enable HSE without bypass*/
	SET_BIT(RCC_CR, RCC_CR_HSE_ON);
	/*wait HSE till be ready*/
	while (!(GET_BIT(RCC_CR,	RCC_CR_HSE_RDY)));

	RCC_CFGR = 0x00000001;

#elif 	FCC_CLOCK_TYPE  ==	RCC_HSE_RC
	//0x00050000
	/*	Enable HSE */
	SET_BIT(RCC_CR, RCC_CR_HSE_ON);
	/*wait HSE till be ready*/
	while (!(GET_BIT(RCC_CR,	RCC_CR_HSE_RDY)));

	/*	External Clock with bypass*/
	SET_BIT(RCC_CR, RCC_CR_HSE_BYP);

	RCC_CFGR = 0x00000001;

#elif 	FCC_CLOCK_TYPE  ==	RCC_HSI
	//0x00000081
	/*Enable HSI*/
	SET_BIT(RCC_CR,	RCC_CR_HSI_ON);
	/*wait HSI till be ready*/
	while (!(GET_BIT(RCC_CR,	RCC_CR_HSI_RDY)));
	RCC_CFGR = 0x00000000;

#elif 	FCC_CLOCK_TYPE  ==	RCC_PLL
	/*Enable PLL*/
	SET_BIT(RCC_CR,	RCC_CR_PLL_ON);

	/* RCC_PLL_INPUT configuration parameter Check start*/
#if		RCC_PLL_INPUT == 	RCC_PLL_IN_HSI_DIV_2
	/*Enable HSI*/
	SET_BIT(RCC_CR,	RCC_CR_HSI_ON);
	/*	Wait HSI till be ready */
	while (!(GET_BIT(RCC_CR,	RCC_CR_HSI_RDY)));

#elif	RCC_PLL_INPUT ==	RCC_PLL_IN_HSE_DIV_2
	/*	Enable HSE */
	SET_BIT(RCC_CR, RCC_CR_HSE_ON);
	/*	Wait HSE till be ready */
	while (!(GET_BIT(RCC_CR,RCC_CR_HSE_RDY)));

#elif	RCC_PLL_INPUT == 	RCC_PLL_IN_HSE
	/*	Enable HSE */
	SET_BIT(RCC_CR, RCC_CR_HSE_ON);
	/*	Wait HSE till be ready */
	while (!(GET_BIT(RCC_CR,	RCC_CR_HSE_RDY)));
	/* RCC_PLL_INPUT configuration parameter Check end*/
#endif
	/* RCC_PLL_MUL_VAL configuration parameter Check start*/
#if RCC_PLL_MUL_VAL >= 2 && RCC_PLL_MUL_VAL <= 16
	/*	Mask PLL Multiplication factor bits in RCC_CFGR*/
	RCC_CFGR = ((RCC_CFGR & RCC_CFGR_PLLMUL_MASK)|(RCC_PLL_MUL_VAL-2));
#else
#error "You chose a Wrong PLL Multiplication Factor!"
	/* RCC_PLL_MUL_VAL configuration parameter Check end*/
#endif
	/*wait PLL till be ready*/
	while (!(GET_BIT(RCC_CR,RCC_CR_PLL_RDY)));
#else
#error "You chose a Wrong Clock type"
	/* FCC_CLOCK_TYPE configuration parameter Check end*/
#endif

	/*	FCC_MCO_OUT configuration parameter Check start*/
#if 	FCC_MCO_OUT == RCC_MCO_NO_CLK
	/*	Mask MCO bits in FCC_CFGR*/
	RCC_CFGR = ((RCC_CFGR & RCC_CFGR_MCO_MASK)|(000));
#elif 	FCC_MCO_OUT == RCC_MCO_SYS_CLK
	/*	Mask MCO bits in FCC_CFGR*/
	RCC_CFGR = ((RCC_CFGR & RCC_CFGR_MCO_MASK)|(0b100));
#elif 	FCC_MCO_OUT == RCC_MCO_HSI
	/*	Mask MCO bits in FCC_CFGR*/
	RCC_CFGR = ((RCC_CFGR & RCC_CFGR_MCO_MASK)|(0b101));
#elif 	FCC_MCO_OUT == RCC_MCO_HSE
	/*	Mask MCO bits in FCC_CFGR*/
	RCC_CFGR = ((RCC_CFGR & RCC_CFGR_MCO_MASK)|(0b110));

#elif 	FCC_MCO_OUT == RCC_MCO_PLL_DIV_2
	/*	Mask MCO bits in FCC_CFGR*/
	RCC_CFGR = ((RCC_CFGR & RCC_CFGR_MCO_MASK)|(0b111));

#else
#error "Wrong MCO output configuration"
	/*	FCC_MCO_OUT configuration parameter Check end*/
#endif
}

void RCC_voidEnableClock ( u8 Copy_u8BusId, u8 Copy_u8PreId ){

	if (31 >= Copy_u8PreId){
		switch (Copy_u8BusId){
		case RCC_AHB : 	SET_BIT(RCC_AHBENR	, Copy_u8PreId	);	break;
		case RCC_APB1:	SET_BIT(RCC_APB1ENR	, Copy_u8PreId	);	break;
		case RCC_APB2:	SET_BIT(RCC_APB2ENR	, Copy_u8PreId	);	break;
		default : /*	Return Error	*/						break;
		}
	} 
	else {

		/*	Return Error	*/
	}
}

void RCC_voidDisableClock ( u8 Copy_u8BusId, u8 Copy_u8PreId ){

	if (31 >= Copy_u8PreId){
		switch (Copy_u8BusId){
		case RCC_AHB : 	CLR_BIT(RCC_AHBENR	, Copy_u8PreId	);	break;
		case RCC_APB1:	CLR_BIT(RCC_APB1ENR	, Copy_u8PreId	);	break;
		case RCC_APB2:	CLR_BIT(RCC_APB2ENR	, Copy_u8PreId	);	break;
		default : /*	Return Error	*/						break;
		}
	} 
	else {

		/*	Return Error	*/
	}
}
