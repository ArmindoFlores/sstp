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
        Body(const Vector& direction, double semi_major_axis, double excentricity);

        Vector position() const;
        OrbitType orbit_type() const;
        const Vector& direction() const;
        double semi_major_axis() const;
        double semi_minor_axis() const;
        double apsis() const;
        double periapsis() const;
        double focal_distance() const;
        double eccentricity() const;
        double eccentric_anomaly() const;
        double angle() const;
        double radius() const;
        void set_angle(double angle);
        void update_orbit(const Vector& direction, double semi_major_axis, double excentricity);
        void update_orbit(double semi_major_axis, double excentricity);

    private:
        double a, b, c, e, theta, i;
        Vector d;
    };
}

#endif