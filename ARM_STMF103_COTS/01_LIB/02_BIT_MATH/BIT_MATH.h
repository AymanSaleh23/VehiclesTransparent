/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:6 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef _BIT_MATH_H_
/*	define this file  */
#define _BIT_MATH_H_

/*	SET_BIT Function Macro */
#define SET_BIT(VAR,BIT)	(VAR |=  (1<< (BIT) ))
/*	CLR_BIT Function Macro */
#define CLR_BIT(VAR,BIT)	(VAR &= ~(1<< (BIT) ))
/*	GET_BIT Function Macro */
#define GET_BIT(VAR,BIT)	(1 & (VAR  >> (BIT) ))
/*	TOG_BIT Function Macro */
#define TOG_BIT(VAR,BIT)	(VAR ^=  (1<< (BIT) ))

/*	end of Preprocessor directive */
#endif
