#include "body.h"
#include <cmath>

const char* SSTP::orbit_type_to_string(SSTP::OrbitType ot)
{
    static const char text[][11] = {"CIRCULAR", "ELLIPTIC", "PARABOLIC", "HYPERBOLIC"};
    return text[std::size_t(ot)];    
}

SSTP::Body::Body(const SSTP::Vector& direction, double a, double e) : a(a), e(e), theta(0), direction(direction)
{
    this->direction *= -1;
    if (direction.dimension() < 2 || direction.dimension() > 3) {
        throw std::invalid_argument(
            "direction should be a 2D or 3D vector (is " + std::to_string(direction.dimension()) + "D)"
        );
    }
    calculate_parameters(this->direction, a, e);
}

SSTP::Vector SSTP::Body::position() const
{
    Vector result{direction.dimension()};
    if (direction.dimension() == 2) {
        double r = radius();
        result[0] = r * std::cos(theta + i);
        result[1] = r * std::sin(theta + i);
    }
    else {
        throw std::invalid_argument("Not implemented!");
    }
    return result;
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

void SSTP::Body::calculate_parameters(const SSTP::Vector& direction, double a, double e)
{
    double l = direction.length();
    if (l != 1) {
        this->direction /= l;
    }

    c = a * e;
    b = std::sqrt(a*a * (1 - e*e));
    i = std::atan2(direction[1], direction[0]);
}