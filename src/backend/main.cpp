#include <cmath>
#include <iostream>
#include <limits>
#include "body.h"
#include "vector.h"

int main()
{
    SSTP::Body body1 {SSTP::Vector{{2, 1}}, 2, 0};
    // SSTP::Body body2 {SSTP::Vector{{2, 1}}, 0.1, 0};

    constexpr int N = 500;
    int stage = 0;
    for (int i = 0; i < N; i++) {
        body1.set_angle(4 * i * M_PI / N);
        if (stage == 0 && body1.angle() >= M_PI) {
            stage = 1;
            double semi_major_axis = body1.semi_major_axis() + 1;
            double eccentricity = 1 - body1.periapsis() / semi_major_axis;
            body1.update_orbit(semi_major_axis, eccentricity);
        }
        if (stage == 1 && body1.angle() >= M_PI * 2) {
            stage = 2;
            double semi_major_axis = body1.apsis();
            double eccentricity = body1.apsis() / semi_major_axis - 1;
            body1.update_orbit(semi_major_axis, eccentricity);
        }
        std::cout << body1.position() << std::endl;
        // body2.set_angle(60 * i * M_PI / N);
        // std::cout << body1.position() + body2.position() << std::endl;
    }
}