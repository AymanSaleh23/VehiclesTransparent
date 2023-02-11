
/************************************************************/
/*					Author : Ayman Saleh					*/
/*					Date   : 22-9-2022						*/
/*					Version: 1.0.0							*/
/************************************************************/

#ifndef TFT_INTERFACE_H_
#define TFT_INTERFACE_H_

void HTFT_voidInit			(void		);
void HTFT_voidDisplayImg	(const u16* Copy_pu16Img	);
void HTFT_voidFillColor		(u16	 	Copy_u16Color	);
void HTFT_voidDrawRectangle (u8 x1, u8 x2, u8 y1, u8 y2 ,u16 Copy_u16BorderColor);
#endif
