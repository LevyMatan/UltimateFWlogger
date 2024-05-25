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


#define PUSHED_EVENTS_LIMIT (10)


// Global variables
static bool g_enable_run_device = true;
static uint32_t g_events_pushed_count = 0;

/*

*/
/**
 * @brief Starts the device.
 *
 * This function initializes the tracer, initializes the device,
 * starts the state machines, and returns 0.
 *
 * @return 0 if the device starts successfully.
 */
int start_device(void) {

    // Initialize the tracer
    trace_status_e status = init_tracer("/workspaces/simple_compiler_project/trace_db.csv");
    handle_tracer_status(status);

    // Initialize the device
    FW_LOG_INFO("Initializing device...");
    state_machine_event_queue_t event_queue = init_device();

    // Start the state machines
    FW_LOG_INFO("Starting state machines...");
    run_device(event_queue);

    return 0;
}

/**
 * Initializes the device by performing the following steps:
 * 1. Initializes the HAL layers.
 * 2. Initializes the event queue.
 *
 * @return The initialized state machine event queue.
 */
state_machine_event_queue_t init_device(void) {
    // Initialize the device
    FW_LOG_INFO("Initializing device...");

    // Initialize the HAL layers
    FW_LOG_INFO("Initializing HAL layers...");
    init_hal();

    // Initialize the event queue
    FW_LOG_INFO("Initializing events queue...");
    state_machine_event_queue_t event_queue = initialize_event_queue(10);
    return event_queue;
}


/**
 * Runs the device and state machines.
 *
 * This function runs the device and state machines by processing events from the event queue.
 * It triggers random events and stops running when the limit of pushed events is reached.
 *
 * @param event_queue The event queue to process events from.
 * @return 0 if the device and state machines were run successfully.
 */
int run_device(state_machine_event_queue_t event_queue) {
    // Run the device
    FW_LOG_INFO("Running device...");
    // Run the state machines
    FW_LOG_INFO("Running state machines...");
    enqueue_event(&event_queue, (state_machine_event_t){MAIN_STATE_MACHINE, EVENT_START});
    while (g_enable_run_device){
        handle_event_queue(&event_queue);
        // Trigger a random event
        int random_event = rand() % 5;
        FW_LOG_INFO("Triggering random event: %s", ENUM_STRING_FROM_TYPE(random_event, "main_state_machine_events"));
        enqueue_event(&event_queue, (state_machine_event_t){MAIN_STATE_MACHINE, random_event});
        g_events_pushed_count++;
        if ( g_events_pushed_count > PUSHED_EVENTS_LIMIT){
            g_enable_run_device = false;
            FW_LOG_INFO("Reached the limit (%d) of pushed events. Stopping the device...", PUSHED_EVENTS_LIMIT);
        }
    }
    return 0;
}

void set_run_device(bool enable) {
    g_enable_run_device = enable;
}

void get_number_of_events_pushed(uint32_t *events_pushed_count) {
    *events_pushed_count = g_events_pushed_count;
}
