
/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:20 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/
#ifndef UART_INTERFACE_H_
#define UART_INTERFACE_H_


void MUART_voidInit		(void);
void MUART_voidTransmit	(u8 *Copy_u8Arr []);
u8	 MUART_u8Receive	(void);
#endif
