
/****************************************************************************/
/*						Author : Ayman Saleh								*/
/*						Date   : 19-9-2022									*/
/*						Version: 1.0.0										*/
/****************************************************************************/


#ifndef S2P_CONFIG_H_
#define S2P_CONFIG_H_
/*	PORT Options:
 * 		GPIO_PORTA
 * 		GPIO_PORTB
 * 		GPIO_PORTC
 * 		GPIO_PORTD
 * 		GPIO_PORTE
 * 		GPIO_PORTF
 * 		GPIO_PORTG
 *
 * 	PIN Options:
 * 		GPIO_PIN0
 * 		GPIO_PIN1
 * 		GPIO_PIN2
 * 		GPIO_PIN3
 * 		GPIO_PIN4
 * 		GPIO_PIN5
 * 		GPIO_PIN6
 * 		GPIO_PIN7
 * 		GPIO_PIN8
 * 		GPIO_PIN9
 * 		GPIO_PIN10
 * 		GPIO_PIN11
 * 		GPIO_PIN12
 * 		GPIO_PIN13
 * 		GPIO_PIN14
 * 	Note: It depends on the Controller
 */
#define SERIAL_DATA		GPIO_PORTA, GPIO_PIN0
#define SHIFT_CLK		GPIO_PORTA, GPIO_PIN1
#define STORAGE_CLK		GPIO_PORTA,	GPIO_PIN2


#endif
