#include <state_machine/state_machine.h>
#include <tracer.h>
#include <unistd.h>


// Global array to hold all state machines:
state_machine_t state_machines[] = {
    {MAIN_STATE_MACHINE, STATE_IDLE, main_state_machine},
};



void main_state_machine(int event) {
    // Main state machine
    FW_LOG_DEBUG("Entered Main state machine with event: %d", event);

    // Main state machine logic
    switch (event) {
        case EVENT_START:
            FW_LOG_INFO("Main state machine started.");
            break;
        case EVENT_STOP:
            FW_LOG_INFO("Main state machine stopped.");
            break;
        case EVENT_PAUSE:
            FW_LOG_INFO("Main state machine paused.");
            break;
        case EVENT_RESUME:
            FW_LOG_INFO("Main state machine resumed.");
            break;
        case EVENT_RESET:
            FW_LOG_INFO("Main state machine reset.");
            break;
        default:
            FW_LOG_ERROR("Main state machine received unknown event: %d", event);
            break;
    }
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

    FW_LOG_DEBUG("Handling event queue...");

    while (event_queue->count > 0) {
        state_machine_event_t event = event_queue->events[event_queue->head];
        FW_LOG_INFO("Handling event: %d for state_machine: %d", event.event, event.type);
        state_machines[event.type].state_machine_func(event.event);
        event_queue->head = (event_queue->head + 1) % event_queue->size;
        event_queue->count--;
    }

    FW_LOG_DEBUG("Event queue handled successfully.");
}

int init_state_machines(void) {
    // Initialize the state machine
    FW_LOG_INFO("Initializing state machine...");

    
    // Initialize the state machine
    FW_LOG_INFO("State machine initialization complete.");

    return 0;
}
