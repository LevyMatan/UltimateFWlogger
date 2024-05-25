// #ifndef __APPLE__
#include <stdio.h>
// #endif


#include <stdint.h>
#include <string.h>

#include "./generated_enum.h"

char type_val_string[1000];

char* get_trace_level_name(void* p_type) {
        uint32_t type = *(uint32_t*)p_type;
        if (type >= sizeof(trace_level_dict) / sizeof(trace_level_dict[0])) {
            return "Invalid type";
        }
    return trace_level_dict[type];
}

char* get_trace_status_name(void* p_type) {
    uint32_t type = *(uint32_t*)p_type;
    if (type >= sizeof(trace_status_dict) / sizeof(trace_status_dict[0])) {
        return "Invalid type";
    }
    return trace_status_dict[type];
}

char* get_state_machines_types_name(void* p_type) {
    uint32_t type = *(uint32_t*)p_type;
    if (type >= sizeof(state_machines_types_dict) / sizeof(state_machines_types_dict[0])) {
        return "Invalid type";
    }
    return state_machines_types_dict[type];
}

char* get_main_state_machine_events_name(void* p_type) {
    uint32_t type = *(uint32_t*)p_type;
    if (type >= sizeof(main_state_machine_events_dict) / sizeof(main_state_machine_events_dict[0])) {
        return "Invalid type";
    }
    return main_state_machine_events_dict[type];
}

char* get_state_machine_states_name(void* p_type) {
    uint32_t type = *(uint32_t*)p_type;
    if (type >= sizeof(state_machine_states_dict) / sizeof(state_machine_states_dict[0])) {
        return "Invalid type";
    }
    return state_machine_states_dict[type];
}

char* get_int_name(void* p_type) {
    int val = *(int *)p_type;
    sprintf(type_val_string, "%d\n", val);
    return type_val_string;
}

char* get_float_name(void* p_type) {
    float val = *(float *)p_type;
    sprintf(type_val_string, "%f\n", val);
    return type_val_string;
}

char* get_double_name(void* p_type) {
    double val = *(double *)p_type;
    sprintf(type_val_string, "%f\n", val);
    return type_val_string;
}

char* get_char_name(void* p_type) {
    char val = *(char *)p_type;
    sprintf(type_val_string, "%c\n", val);
    return type_val_string;
}

char* get_short_name(void* p_type) {
    short val = *(short *)p_type;
    sprintf(type_val_string, "%d\n", val);
    return type_val_string;
}

char* get_long_name(void* p_type) {
    long val = *(long *)p_type;
    sprintf(type_val_string, "%ld\n", val);
    return type_val_string;
}

char* get_long_long_name(void* p_type) {
    long long val = *(long long *)p_type;
    sprintf(type_val_string, "%lld\n", val);
    return type_val_string;
}

getter_func_t g_a_getters[] = {
    get_trace_level_name,
    get_trace_status_name,
    get_state_machines_types_name,
    get_main_state_machine_events_name,
    get_state_machine_states_name,
    get_int_name,
    get_float_name,
    get_double_name,
    get_char_name,
    get_short_name,
    get_long_name,
    get_long_long_name,
};

int typename_to_idx(const char *type_name) {
    if (strcmp(type_name, "trace_level") == 0) return 0;
    if (strcmp(type_name, "trace_status") == 0) return 1;
    if (strcmp(type_name, "state_machines_types") == 0) return 2;
    if (strcmp(type_name, "main_state_machine_events") == 0) return 3;
    if (strcmp(type_name, "state_machine_states") == 0) return 4;
    if (strcmp(type_name, "int") == 0) return 5;
    if (strcmp(type_name, "float") == 0) return 6;
    if (strcmp(type_name, "double") == 0) return 7;
    if (strcmp(type_name, "char") == 0) return 8;
    if (strcmp(type_name, "short") == 0) return 9;
    if (strcmp(type_name, "long") == 0) return 10;
    if (strcmp(type_name, "long_long") == 0) return 11;
    return -1;  // Return -1 if type_name is not found
}
