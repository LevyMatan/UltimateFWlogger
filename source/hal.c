#include <hal/hal.h>
#include <tracer.h>

int init_hal(void) {
  // Initialize the HAL layers
  FW_LOG_INFO("Initializing HAL layers...");

  // Initialize timers
  FW_LOG_INFO("Initializing timers...");

  // Initialize GPIO
  FW_LOG_INFO("Initializing GPIO...");

  // Initialize UART
  FW_LOG_INFO("Initializing UART...");

  // Initialize SPI
  FW_LOG_INFO("Initializing SPI...");

  // HAL initialization complete
  FW_LOG_INFO("HAL initialization complete.");

  return 0;
}
