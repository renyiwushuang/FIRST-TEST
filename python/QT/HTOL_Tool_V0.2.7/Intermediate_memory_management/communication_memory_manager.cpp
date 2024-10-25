#include "communication_memory_manager.h"
#include <stdlib.h>

#include "Intermediate_communication_protocol/communication_common.h"

stRingBuff_t *g_uartTestProtocolReciveRingBuff;

/*******************************************************************************
 *1、Memory Init.
 *******************************************************************************/
int communication_memory_ring_buff_init(RING_BUFF_TYPE_E ringBuffType)
{
    switch (ringBuffType) {
    case MXD_RUN_UART:{
        g_uartTestProtocolReciveRingBuff = creat_ring_buff(RING_SIZE);
        break;
    }
    default: break;
    }
    return 0;
}

/*******************************************************************************
 * 2、Memory Deinit.
 *******************************************************************************/
int communication_memory_ring_buff_deinit(RING_BUFF_TYPE_E ringBuffType)
{
    switch (ringBuffType) {
    case MXD_RUN_UART:{
        free(g_uartTestProtocolReciveRingBuff);
        break;
    }
    default: break;
    }
    return 0;
}
