#include <string.h>

#include "./generated_enum.h"

char* trace_level_dict[4] = {
    "TRACE_LEVEL_DEBUG",
    "TRACE_LEVEL_INFO",
    "TRACE_LEVEL_WARNING",
    "TRACE_LEVEL_ERROR",
};

char* trace_status_dict[5] = {
    "TRACE_STATUS_OK",
    "TRACE_STATUS_FAILED_TO_READ_CONF_FILE",
    "TRACE_STATUS_FAILED_TO_CONVERT_FUNC_STRING",
    "TRACE_STATUS_GENERAL_FAIL",
    "TRACE_STATUS_DEBUG_DISABLED",
};

char* state_machines_types_dict[5] = {
    "MAIN_STATE_MACHINE",
    "SECONDARY_STATE_MACHINE",
    "TERTIARY_STATE_MACHINE",
    "QUATERNARY_STATE_MACHINE",
    "QUINTENARY_STATE_MACHINE",
};

char* main_state_machine_events_dict[5] = {
    "EVENT_START",
    "EVENT_STOP",
    "EVENT_PAUSE",
    "EVENT_RESUME",
    "EVENT_RESET",
};

char* state_machine_states_dict[5] = {
    "STATE_IDLE",
    "STATE_RUNNING",
    "STATE_PAUSED",
    "STATE_STOPPED",
    "STATE_ERROR",
};

