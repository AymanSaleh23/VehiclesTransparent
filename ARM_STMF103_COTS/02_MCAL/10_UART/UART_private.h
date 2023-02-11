
/****************************************************/
/*	Author	:Ayman Saleh							*/
/*	Date	:20 SEP 2022 							*/
/*	Version	:V01		 							*/
/****************************************************/


#ifndef UART_PRIVATE_H_
#define UART_PRIVATE_H_


#define UART1_BASE_ADRESS	(0x40013800)
#define UART2_BASE_ADRESS	(0x40004400)
#define UART3_BASE_ADRESS	(0x40004800)
#define UART4_BASE_ADRESS	(0x40004C00)
#define UART5_BASE_ADRESS	(0x40005000)

typedef struct {
	volatile u32 PE     :1;
	volatile u32 FE     :1;
	volatile u32 NE     :1;
	volatile u32 ORE    :1;
	volatile u32 IDLE   :1;
	volatile u32 RXNE   :1;
	volatile u32 TC     :1;
	volatile u32 TXE    :1;
	volatile u32 LBD    :1;
	volatile u32 CTS	:1;
}SR_bitfields;

typedef union {
	volatile u32 Value;
	volatile SR_bitfields SR_bits;
}SR_t;

typedef struct {
	volatile u32 Fraction	:4;
	volatile u32 Mantissa	:12;
	volatile u32 res		:16;
}BAUD_bitfields;

typedef struct {
	volatile u32 SBK 	:1;
	volatile u32 RWU    :1;
	volatile u32 RE     :1;
	volatile u32 TE     :1;
	volatile u32 IDLEIE :1;
	volatile u32 RXNEIE :1;
	volatile u32 TCIE   :1;
	volatile u32 TXEIE  :1;
	volatile u32 PEIE   :1;
	volatile u32 PS     :1;
	volatile u32 PCE    :1;
	volatile u32 WAKE   :1;
	volatile u32 M      :1;
	volatile u32 UE     :1;
	volatile u32 res	:18;
}CR1_bitfields;


typedef struct {
	volatile u32 ADD		:4;
	volatile u32 res_1		:1;
	volatile u32 LBDL		:1;
	volatile u32 LBDIE		:1;
	volatile u32 res_2		:1;
	volatile u32 LBCL		:1;
	volatile u32 CPHA 		:1;
	volatile u32 CPOL 		:1;
	volatile u32 CLKEN		:1;
	volatile u32 STOP		:2;
	volatile u32 LINEN		:1;
	volatile u32 res_3		:17;
}CR2_bitfields;

typedef struct{
	volatile u32 EIE	:1;
	volatile u32 IREN	:1;
	volatile u32 IRLP	:1;
	volatile u32 HDSEL	:1;
	volatile u32 NACK	:1;
	volatile u32 SCEN	:1;
	volatile u32 DMAR	:1;
	volatile u32 DMAT	:1;
	volatile u32 RTSE	:1;
	volatile u32 CTSE	:1;
	volatile u32 CTSIE	:1;
	volatile u32 res	:21;
}CR3_bitfields;

typedef struct {
	volatile u32 PSC	:8;
	volatile u32 GT		:8;
	volatile u32 res	:16;
}GTPR_bitfields;

typedef struct {
	volatile SR_t 			SR_reg;
	volatile u32 			DR_reg;
	volatile BAUD_bitfields BRR_reg;
	volatile CR1_bitfields 	CR1_reg;
	volatile CR2_bitfields 	CR2_reg;
	volatile CR3_bitfields 	CR3_reg;
	volatile GTPR_bitfields GTPR_reg;
}UART_t;

#define UART1	((volatile UART_t *)(UART1_BASE_ADRESS + 0x00000000))
#define UART2	((volatile UART_t *)(UART2_BASE_ADRESS + 0x00000000))
#define UART3	((volatile UART_t *)(UART3_BASE_ADRESS + 0x00000000))
#define UART4	((volatile UART_t *)(UART4_BASE_ADRESS + 0x00000000))
#define UART5	((volatile UART_t *)(UART5_BASE_ADRESS + 0x00000000))


#define NULL_PTR		(void*)0
#endif
