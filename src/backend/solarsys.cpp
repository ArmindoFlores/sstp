#include "solarsys.h"
#include <cmath>
#include "vector.h"

static double ONE_AU = 1.495978707e11;

/*
All the data aquired from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/
(last updated 27 December 2021)
TODO: more precision digits
*/

// Masses (1e24 kg)
SSTP::Vector mass{{0.330, 4.87, 5.97, 0.073, 0.642, 1898, 568, 86.8, 102, 0.0130}};
// Diameter and Radius (km)
SSTP::Vector diameter{{4879, 12104, 12756, 3475, 6792, 142984, 120536, 51118, 49528, 2376}};
SSTP::Vector radius = diameter / 2;
// Rotation Period (hours)
SSTP::Vector rotation_period{{1407.6, -5832.5, 23.9, 655.7, 24.6, 9.9, 10.7, -17.2, 16.1, -153.3}};
// Perihelion (1e6 km -> au)
SSTP::Vector perihelion = SSTP::Vector{{46.0, 107.5, 147.1, 0.363, 206.7, 740.6, 1357.6, 2732.7, 4471.1, 4436.8}} * 1e6 / ONE_AU;
// Aphelion (1e6 km -> au)
SSTP::Vector aphelion = SSTP::Vector{{69.8, 108.9, 152.1, 0.406, 249.3, 816.4, 1506.5, 3001.4, 4558.9, 7375.9}} * 1e6 / ONE_AU;
// Orbital Inclination (degrees->radians)
SSTP::Vector orbital_inclination = SSTP::Vector{{7.0, 3.4, 0.0, 5.1, 1.8, 1.3, 2.5, 0.8, 1.8, 17.2}} * M_PI / 180;
// Obliquity to Orbit (degrees->radians)
SSTP::Vector obliquity_to_orbit = SSTP::Vector{{0.034, 177.4, 23.4, 6.7, 25.2, 3.1, 26.7, 97.8, 28.3, 122.5}} * M_PI / 180;

const char *SSTP::planet_orbit_to_string(SSTP::PlanetOrbit po)
{
    static const char text[][8] = {"MERCURY", "VENUS", "EARTH", "MOON", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"};
    return text[std::size_t(po)];
}

SSTP::SolarSystem::SolarSystem()
{
    for (size_t i = 0; i < mass.dimension(); i++)
    {
        double a = (aphelion[i] + perihelion[i]) / 2;
        double e = 1 - perihelion[i] / a;
        planets.emplace_back(Vector{{1, 0}}, a, e);
    }
}