#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

typedef enum state_machines_types {
  MAIN_STATE_MACHINE,
  SECONDARY_STATE_MACHINE,
  TERTIARY_STATE_MACHINE,
  QUATERNARY_STATE_MACHINE,
  QUINTENARY_STATE_MACHINE,
} state_machines_types_e;

typedef enum main_state_machine_events {
  EVENT_START,
  EVENT_STOP,
  EVENT_PAUSE,
  EVENT_RESUME,
  EVENT_RESET,
} main_state_machine_events_e;

typedef enum state_machine_states {
  STATE_IDLE,
  STATE_RUNNING,
  STATE_PAUSED,
  STATE_STOPPED,
  STATE_ERROR,
} state_machine_states_e;

typedef struct state_machine {
  state_machines_types_e type;
  state_machine_states_e state;
  void (*state_machine_func)(int event);
} state_machine_t;

typedef struct state_machine_event {
  state_machines_types_e type;
  int event;
} state_machine_event_t;

typedef struct state_machine_event_queue {
  state_machine_event_t *events;
  int size;
  int count;  // Number of events in the queue
  int head;   // Index of the first event in the queue
} state_machine_event_queue_t;

state_machine_event_queue_t initialize_event_queue(int size);
void enqueue_event(state_machine_event_queue_t *event_queue, state_machine_event_t event);
void handle_event_queue(state_machine_event_queue_t *event_queue);

void main_state_machine(int event);

#endif  // STATE_MACHINE_H
