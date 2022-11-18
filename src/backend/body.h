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
        double semi_major_axis() const;
        double semi_minor_axis() const;
        double focal_distance() const;
        double excentricity() const;
        double eccentric_anomaly() const;
        double angle() const;
        double radius() const;
        void set_angle(double angle);

    private:
        double a, b, c, e, theta, i;
        Vector direction;

        void calculate_parameters(const Vector& direction, double semi_major_axis, double excentricity);
    };
}

#endif