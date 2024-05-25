#include <fw_device_mockup/fw_device_mockup.h>

int main(int argc, char *argv[]) {
  // Make a fake use of argc and argv
  (void)argc;
  (void)argv;
  start_device();
  return 0;
}
