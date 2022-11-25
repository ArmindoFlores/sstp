#include "body.h"
#include <cmath>

const char* SSTP::orbit_type_to_string(SSTP::OrbitType ot)
{
    static const char text[][11] = {"CIRCULAR", "ELLIPTIC", "PARABOLIC", "HYPERBOLIC"};
    return text[std::size_t(ot)];    
}

SSTP::Body::Body(const SSTP::Vector& d, double a, double e, double mu) : a(a), e(e), theta(0), mu(mu), n(0), d(d)
{
    if (d.dimension() < 2 || d.dimension() > 3) {
        throw std::invalid_argument(
            "direction should be a 2D or 3D vector (is " + std::to_string(d.dimension()) + "D)"
        );
    }
    update_orbit(this->d, a, e);
}

SSTP::Vector SSTP::Body::position(bool radial) const
{
    Vector result{d.dimension()};
    if (d.dimension() == 2) {
        double r = radius();
        if (radial) {
            result[0] = r;
            result[1] = theta;
        }
        else {
            result[0] = r * std::cos(theta + i);
            result[1] = r * std::sin(theta + i);
        }
    }
    else {
        throw std::invalid_argument("Not implemented!");
    }
    return result;
}

SSTP::Vector SSTP::Body::velocity(bool radial) const
{
    double v = std::sqrt(2 * mu * (1 / radius() - 1 / (2 * a)));
    Vector result(2);
    if (radial) {
        result[0] = v;
        result[1] = theta + i - M_PI_2;
    }
    else {
        result[0] = -v * std::sin(theta + i);
        result[1] = v * std::cos(theta + i);
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

double SSTP::Body::apsis() const
{
    return a * (1 + e);
}

double SSTP::Body::periapsis() const
{
    return a * (1 - e);
}

double SSTP::Body::focal_distance() const
{
    return 2 * c;
}

double SSTP::Body::eccentricity() const
{
    return e;
}

double SSTP::Body::angle() const
{
    return theta;
}

double SSTP::Body::gravitational_parameter() const
{
    return mu;
}

double SSTP::Body::radius() const 
{
    if (e < 1) {
        return a * (1 - e*e) / (1 + e * std::cos(theta));
    }
    return a * (e*e - 1) / (1 + e * std::cos(theta));
}

double SSTP::Body::inclination() const 
{
    return i;
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

SSTP::Vector SSTP::Body::direction() const
{
    return -1*d;
}

void SSTP::Body::set_angle(double angle)
{
    theta = angle;
}

void SSTP::Body::set_gravitational_parameter(double mu)
{
    this->mu = mu;
}

void SSTP::Body::update_orbit(const SSTP::Vector& d, double a, double e)
{
    this->a = a;
    this->e = e;

    this->d = -1 * d;
    double l = this->d.length();
    if (l != 1) {
        this->d /= l;
    }

    c = a * e;
    b = std::sqrt(a*a * (1 - e*e));
    i = std::atan2(this->d[1], this->d[0]);
    n = std::sqrt(mu / std::pow(a, 3));
}

void SSTP::Body::update_orbit(double a, double e)
{
    this->a = a;
    this->e = e;
    c = a * e;
    b = std::sqrt(a*a * (1 - e*e));
    n = std::sqrt(mu / std::pow(a, 3));
}

void SSTP::Body::timestep(double ts)
{
    theta += n * ts;
}