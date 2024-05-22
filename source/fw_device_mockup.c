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
#include <tracer.h>
#include <fw_device_mockup/fw_device_mockup.h>
#include <hal/hal.h>



int start_device(void) {
    
    // Initialize the tracer
    trace_status_e status = init_tracer("/workspaces/simple_compiler_project/trace_db.csv");
    handle_tracer_status(status);

    // Start the device
    FW_LOG_INFO("Starting device...");

    // Initialize the device
    FW_LOG_INFO("Initializing device...");
    return init_device();
}

int init_device(void) {
    // Initialize the device
    FW_LOG_INFO("Initializing device...");

    // Initialize the state machines
    FW_LOG_INFO("Initializing state machines...");

    // Initialize the HAL layers
    FW_LOG_INFO("Initializing HAL layers...");
    init_hal();

    return 0;
}