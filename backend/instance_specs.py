# Instance specifications used by GreenOps.
#
# These are simplified values for our MVP.
# They are not intended to represent exact AWS pricing
# or production hardware specifications.

INSTANCE_SPECS = {

    "m5.large": {
        "vcpus": 2,
        "ram_gb": 8,
        "price_per_hour": 5,
        "power_watts": 100
    },

    "m5.xlarge": {
        "vcpus": 4,
        "ram_gb": 16,
        "price_per_hour": 10,
        "power_watts": 180
    },

    "m5.2xlarge": {
        "vcpus": 8,
        "ram_gb": 32,
        "price_per_hour": 20,
        "power_watts": 250
    }
}