/*
This file is the entry point to the mockup of a device firmware.
It contains the main function and the init_tracer function.
The mockup firmware will contain few state machines and HAL layers that won't do much.
But they will spin in a loop and print debug messages.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>

#include <tracer.h>
#include <fw_device_mockup/fw_device_mockup.h>
#include <state_machine/state_machine.h>
#include <hal/hal.h>



int start_device(void) {
    
    // Initialize the tracer
    trace_status_e status = init_tracer("/workspaces/simple_compiler_project/trace_db.csv");
    handle_tracer_status(status);

    // Start the device
    FW_LOG_INFO("Starting device...");

    // Initialize the device
    FW_LOG_INFO("Initializing device...");
    state_machine_event_queue_t event_queue = init_device();

    // Start the state machines
    FW_LOG_INFO("Starting state machines...");
    run_device(event_queue);

    return 0;

}

state_machine_event_queue_t init_device(void) {
    // Initialize the device
    FW_LOG_INFO("Initializing device...");

    // Initialize the state machines
    FW_LOG_INFO("Initializing state machines...");

    // Initialize the HAL layers
    FW_LOG_INFO("Initializing HAL layers...");
    init_hal();

    // Initialize the event queue
    state_machine_event_queue_t event_queue = initialize_event_queue(10);
    return event_queue;
}


int run_device(state_machine_event_queue_t event_queue) {
    // Run the device
    FW_LOG_INFO("Running device...");
    // Run the state machines
    FW_LOG_INFO("Running state machines...");
    enqueue_event(&event_queue, (state_machine_event_t){MAIN_STATE_MACHINE, EVENT_START});
    while (true){
        handle_event_queue(&event_queue);
        // Trigger a random evvent
        int random_event = rand() % 5;
        FW_LOG_INFO("Triggering random event: %d", random_event);
        enqueue_event(&event_queue, (state_machine_event_t){MAIN_STATE_MACHINE, random_event});
    }
    return 0;
}