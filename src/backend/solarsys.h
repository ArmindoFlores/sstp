#ifndef _SOLARSYS_H_
#define _SOLARSYS_H_

#include <vector>
#include "body.h"
#include "vector.h"

namespace SSTP
{
    enum class PlanetOrbit
    {
        MERCURY,
        VENUS,
        EARTH,
        MOON,
        MARS,
        JUPITER,
        SATURN,
        URANUS,
        NEPTUNE,
        PLUTO
    };

    const char *planet_orbit_to_string(PlanetOrbit);

    /*
    This class is used to describe the solar system.
    */
    class SolarSystem
    {
    public:
        SolarSystem();

    private:
        std::vector<Body> planets;
    };
}

#endif