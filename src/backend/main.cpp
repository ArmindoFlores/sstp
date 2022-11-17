#include <cmath>
#include <iostream>
#include <limits>
#include "body.h"

int main()
{
    SSTP::Body body {SSTP::Vector({-1.0, 0.0}), SSTP::Vector({1.0, 0.0}), 6};
    std::cout << "2a = " << 2*body.semi_major_axis() << std::endl;
    std::cout << "2b = " << 2*body.semi_minor_axis() << std::endl;
    std::cout << "2c = " << body.focal_distance() << std::endl;
    std::cout << "e = " << body.excentricity() << std::endl;
    std::cout << "Orbit type: " << SSTP::orbit_type_to_string(body.orbit_type()) << std::endl << std::endl;

    body.set_angle(0);
    std::cout << "\u03b8 = 0 rad:" << std::endl;
    std::cout << "\tPosition: " << body.position() << std::endl << std::endl;

    body.set_angle(M_PI / 2);
    std::cout << "\u03b8 = \u03c0/2 rad:" << std::endl;
    std::cout << "\tPosition: " << body.position() << std::endl << std::endl;

    body.set_angle(M_PI);
    std::cout << "\u03b8 = \u03c0 rad:" << std::endl;
    std::cout << "\tPosition: " << body.position() << std::endl << std::endl;

    body.set_angle(3 * M_PI / 2);
    std::cout << "\u03b8 = 3\u03c0/2 rad:" << std::endl;
    std::cout << "\tPosition: " << body.position() << std::endl << std::endl;

}