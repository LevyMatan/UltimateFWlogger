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
    default: "unknown")
typedef char* (*getter_func_t)(void*);
extern char type_val_string[1000];

extern char* get_trace_level_name(void* p_type);
extern char* trace_level_dict[4];
extern char* get_trace_status_name(void* p_type);
extern char* trace_status_dict[5];
extern getter_func_t g_a_getters[];
int typename_to_idx(const char *type_name);
