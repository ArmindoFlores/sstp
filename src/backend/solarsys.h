#ifndef _SOLARSYS_H_
#define _SOLARSYS_H_

#include <vector>
#include "body.h"
#include "vector.h"

#define ONE_AU 1.495978707e11

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
        const std::vector<Body>& get_planets() const;
        void add_satellite(const Body& satellite);
        const std::vector<Body>& get_satellites() const;
        void timestep(double ts);

    private:
        std::vector<Body> planets, satellites;
    };
}

#endif