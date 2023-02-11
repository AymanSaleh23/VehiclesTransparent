/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:16 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/

/*	Header File Guard
	if file is not defined 
 */
#ifndef _OS_PRIVATE_H_
/*	define this file  */
#define _OS_PRIVATE_H_

#define RUNNING		1
#define WAITING		2
#define SUSPEND		3
#define TERMINATED	4
#define READY		5

#define NULL_PTR ((void *) (0))
static void SOS_voidSheduler (void);

#endif
