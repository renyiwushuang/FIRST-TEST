#ifndef COMMUNICATION_MEMORY_MANAGER_H
#define COMMUNICATION_MEMORY_MANAGER_H

typedef enum
{
    MXD_RUN_UART,

}RING_BUFF_TYPE_E;

/*******************************************************************************
 * 1、Memory Init.
 *******************************************************************************/
extern int communication_memory_ring_buff_init(RING_BUFF_TYPE_E ringBuffType);

/*******************************************************************************
 * 2、Memory Deinit.
 *******************************************************************************/
extern int communication_memory_ring_buff_deinit(RING_BUFF_TYPE_E ringBuffType);

#endif  //COMMUNICATION_MEMORY_MANAGER_H
