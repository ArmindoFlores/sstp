#include <chrono>
#include <cmath>
#include <iostream>
#include <limits>
#include "body.h"
#include "vector.h"
#include "maneuvers.h"
#include "solarsys.h"
#include "ipc.h"

int main()
{
    // SSTP::Body body1 {SSTP::Vector{{1, 0}}, 11500, 0.5, 3.25e5};
    // SSTP::Body body2 {SSTP::Vector{{1, 0}}, 6600, 0.5, 3.25e5};

    // body1.set_angle(0);
    // body2.set_angle(M_PI);

    // auto result = SSTP::hohmann_transfer(body1, body2);

    // std::cout << result.deltav[0] << std::endl;
    // std::cout << result.deltav[1] << std::endl;
    // std::cout << "Delta-V total = " << result.deltav[0].length()+result.deltav[1].length() << " km/s" << std::endl;

    // body1.set_angle(-M_PI/2);
    // std::cout << "v = " << body1.velocity() << std::endl;

    SSTP::IPCServer server("/tmp/sstp_socket");
    server.setup();

    auto start = std::chrono::high_resolution_clock::now();
    std::thread server_thread {[&server]{ while (true) {server.main_loop();}}};
    server_thread.detach();

    while (true) {
        auto stop = std::chrono::high_resolution_clock::now();
        auto ts = (stop - start).count() / 1e9 * 60 * 60 * 24;
        start = stop;
        std::cout << "TS update: " << ts << std::endl;
        server.solar_system().timestep(ts);
    }
    
    // for (size_t i = 0; i < 5000; i++) {
    //     ss.timestep(60 * 60 * 24);
    //     const auto& planets = ss.get_planets();
    //     for (size_t p = 0; p < planets.size(); p++) {
    //         const auto& planet = planets[p];
    //         std::cout << "i = " << i << "\t" << "p = " << p << " " << planet.position() / ONE_AU << "\n";
    //     }
    // }
    
}