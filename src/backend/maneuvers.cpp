#include "maneuvers.h"

#include <cmath>
#include <iostream>

SSTP::Vector SSTP::orbit_velocity(const Body& orbit, double mu)
{
    double v = std::sqrt(2 * mu * (1 / orbit.radius() - 1 / (2 * orbit.semi_major_axis())));
    SSTP::Vector result{{
        -v * std::sin(orbit.angle() + orbit.inclination()), 
        v * std::cos(orbit.angle() + orbit.inclination())
    }};
    return result;
}

SSTP::HohmannInfo SSTP::hohmann_transfer(const Body& orbit1, const Body& orbit2, double mu)
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
    Body transfer_orbit {orbit1.direction(), a, e};
    auto deltav1 = orbit_velocity(transfer_orbit, mu) - orbit_velocity(orbit1, mu);
    transfer_orbit.set_angle(M_PI);
    auto deltav2 = orbit_velocity(orbit2, mu) - orbit_velocity(transfer_orbit, mu);
    return {
        {0, M_PI}, 
        {deltav1, deltav2},
        transfer_orbit
    };
}