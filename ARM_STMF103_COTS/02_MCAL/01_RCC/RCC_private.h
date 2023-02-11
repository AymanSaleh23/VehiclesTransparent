/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:6 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef _RCC_PRIVATE_H_
/*	define this file  */
#define _RCC_PRIVATE_H_

/*	
	Register Definition Way 1
	Base Address :	0x4002100	
*/

/*	Congfigure Clock for Processor  Register
	Enable/Disable Clock System (HSE, HSI, PLL).
	No ristriction for enabling all Clock types.
	This Register Doesn't mention which type will join to Processor.
*/
#define RCC_CR			*((u32*) (0x40021000))

/*PLL_RDY: PLL clock ready flag
	0: PLL unlocked
	1: PLL locked
	Access: R
	Note: Set By HW, about no time need to settling time 
*/
#define RCC_CR_PLL_RDY		25
/*PLL_ON: PLL enable
	0: PLL Off
	1: PLL On
	Access: RW
	Note: can't be reset if choosed to be the system clock.
*/
#define RCC_CR_PLL_ON		24
/*CSS_ON: Clock security system enable
	0: Clock detector OFF
	1: Clock detector ON	
	Access: RW
	Note: Clock detector for test the oscilator behavior
*/
#define RCC_CR_CSS_ON	19
/*HSEBYP: External high-speed clock bypass
	0: external 4-16 MHz oscillator not bypassed
	1: external 4-16 MHz oscillator bypassed with external clock
	Access: RW
	Note:
		- The external clock must be enabled with the HSEON bit set, to be used by the device
		- The HSEBYP bit can be written only if the HSE oscillator is disabled
*/
#define RCC_CR_HSE_BYP	18
/*HSERDY: External high-speed clock ready flag
	0: HSE oscillator not ready
	1: HSE oscillator ready
	Access: R
	Note: 
		- This bit needs 6 cycles of the 
		- HSE oscillator clock to fall down after HSEON reset.
*/
#define RCC_CR_HSE_RDY	17
/*HSEON: HSE clock enable
	0: HSE oscillator OFF
	1: HSE oscillator ON
	Access: RW
	Note:	This bit cannot be reset if the HSE oscillator is used directly or indirectly as the system clock.
*/
#define RCC_CR_HSE_ON	16
/*HSIRDY: Internal high-speed clock ready flag
	0: internal 8 MHz RC oscillator not ready
	1: internal 8 MHz RC oscillator ready
	Access: R
	Note: 
		- HSI is Default System Clock type.
		- Set by hardware to indicate that internal 8 MH.
		- HSIRDY goes low after 6 internal 8 MHz RC oscillator clock cycles

*/
#define RCC_CR_HSI_RDY	1
/*HSION: Internal high-speed clock enable
	0: internal 8 MHz RC oscillator OFF
	1: internal 8 MHz RC oscillator ON
	Access: RW
	Note:
		- Default System Clock.
		- Set by hardware to force the internal 8 MHz RC oscillator ON
		- Turn RC 8-MHz On when:
			* Leaving Stop 
			* Standby mode 
			* Failure of the external 4-16 MHz oscillator used directly or indirectly as system clock (after multiplication factor in PLL).
		- This bit cannot be reset if the internal 8 MHz RC is used directly or indirectly as system clock or is selected to become the system clock
*/
#define RCC_CR_HSI_ON	0

#define RCC_CR_HSITRIM_MASK		0xffffff07	//0b 1111 1111 1111 1111 1111 1111 0000 0111
#define RCC_CR_HSICAL_MASK		0xffff00ff	//0b 1111 1111 1111 1111 0000 0000 1111 1111

/*	Congfigure Clock for Processor  Register
	Decide which Clock type (HSE, HSI, PLL) will join to Processor.	
*/
#define RCC_CFGR		*((u32*) (0x40021004))
#define RCC_CFGR_USBPRE		22
#define RCC_CFGR_PLLXTPRE	17
#define RCC_CFGR_PLLSRC		16
#define RCC_CFGR_SW_MASK		0xfffffffc //0b 1111 1111 1111 1111 1111 1111 1111 1100
#define RCC_CFGR_SWS_MASK		0xfffffff3 //0b 1111 1111 1111 1111 1111 1111 1111 0011
#define RCC_CFGR_HPRE_MASK		0xffffff0f //0b 1111 1111 1111 1111 1111 1111 0000 1111
#define RCC_CFGR_PPRE1_MASK		0xfffff8ff //0b 1111 1111 1111 1111 1111 1000 1111 1111
#define RCC_CFGR_PPRE2_MASK		0xffffc7ff //0b 1111 1111 1111 1111 1100 0111 1111 1111
#define RCC_CFGR_ADCPRE_MASK	0xffff3fff //0b 1111 1111 1111 1111 0011 1111 1111 1111
#define RCC_CFGR_PLLMUL_MASK	0xffc3ffff //0b 1111 1111 1100 0011 1111 1111 1111 1111
#define RCC_CFGR_MCO_MASK		0xf8ffffff //0b 1111 1000 1111 1111 1111 1111 1111 1111


#define RCC_CIR			*((u32*) (0x40021008))
#define RCC_APB2RSTR	*((u32*) (0x4002100C))
#define RCC_APB1RSTR	*((u32*) (0x40021010))

/*	Enable/Disable Clock for Peripherals  Register*/
#define RCC_AHBENR		*((u32*) (0x40021014))
/*	Enable/Disable Clock for Peripherals  Register*/
#define RCC_APB2ENR		*((u32*) (0x40021018))
/*	Enable/Disable Clock for Peripherals  Register*/
#define RCC_APB1ENR		*((u32*) (0x4002101C))


#define RCC_BDCR		*((u32*) (0x40021020))
#define RCC_CSR			*((u32*) (0x40021024))


/*	Clock Types */
#define RCC_HSE_RC			1
#define RCC_HSE_CRYSTAL		2
#define RCC_HSI				3
#define RCC_PLL				4

/*	PLL input options */
#define RCC_PLL_IN_HSI_DIV_2	1
#define RCC_PLL_IN_HSE_DIV_2	2
#define RCC_PLL_IN_HSE			3

/*	MOC Pin output Options */
#define RCC_MCO_NO_CLK			1
#define RCC_MCO_SYS_CLK			2
#define RCC_MCO_HSI				3
#define RCC_MCO_HSE				4
#define RCC_MCO_PLL_DIV_2		5

/*	end of Preprocessor directive */
#endif
