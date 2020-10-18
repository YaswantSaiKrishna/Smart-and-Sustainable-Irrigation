#define SIG A0                            /* Assign SIG pin as Analog output for all 16 channels of Multiplexer to pin A0 of NodeMCU */

typedef enum {
    S0        = 0,                        /* Assign Multiplexer pin S0 connect to pin D0 of NodeMCU */
    S1        = 1,                        /* Assign Multiplexer pin S1 connect to pin D1 of NodeMCU */
    S2        = 2,                        /* Assign Multiplexer pin S2 connect to pin D2 of NodeMCU */
    S3        = 3,                        /* Assign Multiplexer pin S3 connect to pin D3 of NodeMCU */
    S4        = 4,                        /* Assign Motor pin S4 connect to pin D4 of NodeMCU */
} gpio_pins;
