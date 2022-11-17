#include "body.h"
#include <cmath>

const char* SSTP::orbit_type_to_string(SSTP::OrbitType ot)
{
    static const char text[][11] = {"CIRCULAR", "ELLIPTIC", "PARABOLIC", "HYPERBOLIC"};
    return text[std::size_t(ot)];    
}

SSTP::Body::Body(const SSTP::Vector& f1, const SSTP::Vector& f2, double a) : a(a), f1(f1), f2(f2)
{
    if (f1.dimension() != f2.dimension()) {
        throw std::invalid_argument(
            "f1 and f2 should have the same dimension (" + std::to_string(f1.dimension()) + " != " + std::to_string(f2.dimension()) + ")"
        );
    }
    if (f1.dimension() < 2 || f1.dimension() > 3) {
        throw std::invalid_argument(
            "f1 and f2 should be 2D or 3D vectors (were " + std::to_string(f1.dimension()) + "D)"
        );
    }
    calculate_parameters(f1, f2, a);
}

SSTP::Vector SSTP::Body::position() const
{
    Vector result ({f1.dimension()});
    if (result.dimension() == 2) {
        double r = radius();
        result[0] = r * std::cos(theta + i);
        result[1] = r * std::sin(theta + i);
    }
    else {
        throw std::invalid_argument("Not implemented!");
    }
    return f2 + result;
}

double SSTP::Body::semi_major_axis() const
{
    return a;
}

double SSTP::Body::semi_minor_axis() const
{
    return b;
}

double SSTP::Body::focal_distance() const
{
    return 2 * c;
}

double SSTP::Body::excentricity() const
{
    return e;
}

double SSTP::Body::angle() const
{
    return theta;
}

double SSTP::Body::radius() const 
{
    return a * (1 - e*e) / (1 + e * std::cos(theta));
}

double SSTP::Body::eccentric_anomaly() const
{
    return std::atan2(std::sqrt(1 - e*e) * std::sin(theta), e + std::cos(theta));
}

SSTP::OrbitType SSTP::Body::orbit_type() const
{
    if (e == 0) {
        return OrbitType::CIRCULAR;
    }
    if (e < 1) {
        return OrbitType::ELLIPTIC;
    }
    if (e == 1) {
        return OrbitType::PARABOLIC;
    }
    return OrbitType::HYPERBOLIC;
}

void SSTP::Body::set_angle(double angle)
{
    theta = angle;
}

void SSTP::Body::calculate_parameters(const SSTP::Vector& f1, const SSTP::Vector& f2, double a)
{
    c = (f1 - f2).length() / 2;
    e = c / a;
    b = std::sqrt(a*a * (1 - e*e));

    Vector displacement = f2 - f1;
    i = std::atan2(displacement[1], displacement[0]);
    theta = 0;
}