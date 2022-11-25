#include "maneuvers.h"

#include <cmath>
#include <iostream>


SSTP::HohmannInfo SSTP::hohmann_transfer(const Body& orbit1, const Body& orbit2)
{
    double angle1 = orbit1.inclination(), angle2 = orbit2.inclination();
    if (angle1 != angle2) {
        throw std::invalid_argument(
            "Orbits must have the same orientation (" + std::to_string(angle1) + " != " + std::to_string(angle2) + ")"
        );
    }

    double periapsis = orbit1.periapsis();
    double a = (periapsis + orbit2.apsis()) / 2.0;
    double e = 1 - periapsis / a;
    Body transfer_orbit {orbit1.direction(), a, e, orbit1.gravitational_parameter()};
    auto deltav1 = transfer_orbit.velocity() - orbit1.velocity();
    transfer_orbit.set_angle(M_PI);
    auto deltav2 = orbit2.velocity() - transfer_orbit.velocity();
    return {
        {0, M_PI}, 
        {deltav1, deltav2},
        transfer_orbit
    };
}