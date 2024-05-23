#define typename(x) _Generic((x), \
    int: "int", \
    float: "float", \
    double: "double", \
    char: "char", \
    short: "short", \
    long: "long", \
    long long: "long long", \
    enum trace_level: "trace_level", \
    enum trace_status: "trace_status", \
    enum state_machines_types: "state_machines_types", \
    enum main_state_machine_events: "main_state_machine_events", \
    enum state_machine_states: "state_machine_states", \
    default: "unknown")
typedef char* (*getter_func_t)(void*);
extern char type_val_string[1000];

extern char* get_trace_level_name(void* p_type);
extern char* trace_level_dict[4];
extern char* get_trace_status_name(void* p_type);
extern char* trace_status_dict[5];
extern char* get_state_machines_types_name(void* p_type);
extern char* state_machines_types_dict[5];
extern char* get_main_state_machine_events_name(void* p_type);
extern char* main_state_machine_events_dict[5];
extern char* get_state_machine_states_name(void* p_type);
extern char* state_machine_states_dict[5];
extern getter_func_t g_a_getters[];
int typename_to_idx(const char *type_name);
