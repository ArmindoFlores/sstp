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
        Body(const Vector& f1, const Vector& f2, double semi_major_axis);

        Vector velocity() const;
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
        double a, b, c, e, theta, r, i;
        Vector f1, f2;

        void calculate_parameters(const Vector& f1, const Vector& f2, double semi_major_axis);
        double r_from_theta() const;
    };
}

#endif