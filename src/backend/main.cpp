#include <cmath>
#include <iostream>
#include <limits>
#include "body.h"
#include "vector.h"
#include "maneuvers.h"
#include "solarsys.h"

int main()
{
    // SSTP::Body body1 {SSTP::Vector{{0, 1}}, 11500, 0, 3.25e5};
    // SSTP::Body body2 {SSTP::Vector{{0, 1}}, 6600, 0, 3.25e5};

    // body1.set_angle(0);
    // body2.set_angle(M_PI);

    // auto result = SSTP::hohmann_transfer(body1, body2);

    // std::cout << result.deltav[0] << std::endl;
    // std::cout << result.deltav[1] << std::endl;
    // std::cout << "Delta-V total = " << result.deltav[0].length()+result.deltav[1].length() << " km/s" << std::endl;

    SSTP::SolarSystem ss;
    
    for (size_t i = 0; i < 5000; i++) {
        ss.timestep(60 * 60 * 24);
        const auto& planets = ss.get_planets();
        for (size_t p = 0; p < planets.size(); p++) {
            const auto& planet = planets[p];
            std::cout << "i = " << i << "\t" << "p = " << p << " " << planet.position() / ONE_AU << "\n";
        }
    }
    
}