#ifndef _MANEUVERS_H_
#define _MANEUVERS_H_

#include <array>
#include "vector.h"
#include "body.h"

namespace SSTP {
    struct HohmannInfo {
        std::array<double, 2> theta;
        std::array<Vector, 2> deltav;
        Body transfer_orbit;
    };

    Vector orbit_velocity(const Body& orbit, double mu);
    HohmannInfo hohmann_transfer(const Body& orbit1, const Body& orbit2, double mu);
}

#endif
