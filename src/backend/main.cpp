#include <cmath>
#include <iostream>
#include <limits>
#include "body.h"
#include "ipc.h"

int main()
{
    // SSTP::Body body {SSTP::Vector({-0.7, -0.7}), SSTP::Vector({0.7, 0.7}), 0.8};

    // constexpr int N = 1000;
    // for (int i = 0; i < N; i++) {
    //     body.set_angle(i * 1.5 * M_PI / N - M_PI * 0.75);
    //     std::cout << body.position() << std::endl;
    // }

    SSTP::IPCServer server {"/tmp/sstp_socket"};
    bool status = server.setup();
    std::cout << "Status: " << status << std::endl;;
    
    if (!status)
        return 1;

    while (server.main_loop()) {
        std::cout << "Looping..." << std::endl;
    }

}