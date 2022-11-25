#ifndef _BODY_H_
#define _BODY_H_

#include "vector.h"

namespace SSTP {
    enum class OrbitType {
        CIRCULAR,
        ELLIPTIC,
        PARABOLIC,
        HYPERBOLIC
    };

    const char* orbit_type_to_string(OrbitType);

    /*
    This class is used to describe a body following an elliptical, parabolic or 
    hyperbolic orbit.
    */
    class Body {
    public:
        Body(const Vector& direction, double semi_major_axis, double eccentricity, double gravitational_parameter);

        Vector position(bool radial=false) const;
        Vector velocity(bool radial=false) const;
        OrbitType orbit_type() const;
        Vector direction() const;
        double semi_major_axis() const;
        double semi_minor_axis() const;
        double apsis() const;
        double periapsis() const;
        double focal_distance() const;
        double eccentricity() const;
        double eccentric_anomaly() const;
        double angle() const;
        double gravitational_parameter() const;
        double radius() const;
        double inclination() const;
        void set_angle(double angle);
        void set_gravitational_parameter(double mu);
        void update_orbit(const Vector& direction, double semi_major_axis, double excentricity);
        void update_orbit(double semi_major_axis, double excentricity);
        void timestep(double ts);

    private:
        double a, b, c, e, theta, i, mu, n;
        Vector d;
    };
}

#endif