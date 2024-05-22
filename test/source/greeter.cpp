#include <doctest/doctest.h>
#include <fw_device_mockup/fw_device_mockup.h>

#include <string>

TEST_CASE("FwDeviceMockup") {
    int ret = start_device();
    CHECK(ret == 0);
}
