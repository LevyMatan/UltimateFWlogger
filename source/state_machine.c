#include <state_machine/state_machine.h>
#include <tracer.h>
#include <unistd.h>
#include <stdlib.h>

// Global array to hold all state machines:
static state_machine_t state_machines[] = {
    {MAIN_STATE_MACHINE, STATE_IDLE, main_state_machine},
};



void main_state_machine(int event) {

    // Cache the current state
    state_machine_states_e current_state = state_machines[MAIN_STATE_MACHINE].state;

    // Main state machine
    FW_LOG_INFO("Entered Main state machine at state: %s with event: %s", ENUM_STRING(current_state), ENUM_STRING_FROM_TYPE(event, "main_state_machine_events"));


    // Initialize the next state
    state_machine_states_e next_state = current_state;

    // Main state machine logic
    switch (event) {
        case EVENT_START:
            FW_LOG_INFO("Main state machine started.");
            next_state = STATE_RUNNING;
            break;
        case EVENT_STOP:
            FW_LOG_INFO("Main state machine stopped.");
            next_state = STATE_STOPPED;
            break;
        case EVENT_PAUSE:
            FW_LOG_INFO("Main state machine paused.");
            next_state = STATE_PAUSED;
            break;
        case EVENT_RESUME:
            FW_LOG_INFO("Main state machine resumed.");
            next_state = STATE_RUNNING;
            break;
        case EVENT_RESET:
            FW_LOG_INFO("Main state machine reset.");
            next_state = STATE_IDLE;
            break;
        default:
            FW_LOG_ERROR("Main state machine received unknown event: %d", event);
            break;
    }

    // Update the state
    state_machines[MAIN_STATE_MACHINE].state = next_state;
}


state_machine_event_queue_t initialize_event_queue(int size) {
    FW_LOG_DEBUG("Initializing event queue with size: %d", size);
    // Initialize the event queue
    state_machine_event_queue_t event_queue;
    event_queue.events = (state_machine_event_t *)malloc(size * sizeof(state_machine_event_t));
    event_queue.size = size;
    event_queue.count = 0;
    event_queue.head = 0;

    return event_queue;
}

void enqueue_event(state_machine_event_queue_t *event_queue, state_machine_event_t event)
{
    if (event_queue == NULL) {
        FW_LOG_ERROR("Event queue is NULL. Cannot enqueue event.");
        return;
    }
    FW_LOG_INFO("Enqueuing event: %d for state_machine: %d", event.event, event.type);

    int write_index = (event_queue->head + event_queue->count) % event_queue->size;
    if(event_queue->count + 1 >= event_queue->size) {
        FW_LOG_ERROR("Event queue is full. Will override the newest event.");
        state_machine_event_t *event_to_override = &event_queue->events[write_index];
        FW_LOG_WARN("Override the event: %d for state_machine: %d", event_to_override->event, event_to_override->type);
        event_to_override->event = event.event;
        event_to_override->type = event.type;
    }
    else{
        event_queue->events[write_index] = event;
        event_queue->count++;
    }

    FW_LOG_DEBUG("Event enqueued successfullyat index: %d", write_index);
}

void handle_event_queue(state_machine_event_queue_t *event_queue)
{
    if (event_queue == NULL) {
        FW_LOG_ERROR("Event queue is NULL. Cannot handle event queue.");
        return;
    }

    FW_LOG_INFO("Handling event queue...");

    while (event_queue->count > 0) {
        state_machine_event_t event = event_queue->events[event_queue->head];
        FW_LOG_INFO("Handling event: %s for state_machine: %s", ENUM_STRING_FROM_TYPE(event.event, "main_state_machine_events"), ENUM_STRING(event.type));
        state_machines[event.type].state_machine_func(event.event);
        event_queue->head = (event_queue->head + 1) % event_queue->size;
        event_queue->count--;
    }

    FW_LOG_DEBUG("Event queue handled successfully.");
}
