#include "vector.h"
#include <cmath>
#include <numeric>

SSTP::Vector::Vector(std::size_t N) : vec(N), dim(N) {}
SSTP::Vector::Vector(const double* arr, std::size_t N) : vec(arr, arr+N*sizeof(double)), dim(N) {}
SSTP::Vector::Vector(const std::vector<double>& vec) : vec(vec), dim(vec.size()) {}
SSTP::Vector::Vector(const Vector& vec) : vec(vec.vec), dim(vec.dim) {}
SSTP::Vector::Vector(Vector&& vec) : dim(vec.dim) { this->vec = std::move(vec.vec); }

std::size_t SSTP::Vector::dimension() const {
    return dim;
}

double SSTP::Vector::length() const {
    return std::sqrt(std::inner_product(vec.begin(), vec.end(), vec.begin(), 0.0));
}

SSTP::Vector SSTP::Vector::normalized() const {
    double l = length();
    if (l == 0) {
        throw std::domain_error("Cannot normalize a 0-length vector");
    }
    Vector result{*this};
    result /= l;
    return result;
}

double& SSTP::Vector::operator[](std::size_t i)
{
    return vec[i];
}

double SSTP::Vector::operator[](std::size_t i) const
{
    return vec[i];
}

SSTP::Vector& SSTP::Vector::operator+=(double x)
{
    for (size_t i = 0; i < vec.size(); i++) {
        vec[i] += x;
    }
    return *this;
}

SSTP::Vector& SSTP::Vector::operator+=(const Vector& v)
{
    if (v.dim != dim) {
        throw std::out_of_range(
            "Tried to add vectors of different size (" + std::to_string(dim) + " != " + std::to_string(v.dim) + ")"
        );
    }
    for (size_t i = 0; i < vec.size(); i++) {
        vec[i] += v[i];
    }
    return *this;
}

SSTP::Vector& SSTP::Vector::operator-=(double x)
{
    for (size_t i = 0; i < vec.size(); i++) {
        vec[i] -= x;
    }
    return *this;
}

SSTP::Vector& SSTP::Vector::operator-=(const Vector& v)
{
    if (v.dim != dim) {
        throw std::out_of_range(
            "Tried to subtract vectors of different size (" + std::to_string(dim) + " != " + std::to_string(v.dim) + ")"
        );
    }
    for (size_t i = 0; i < vec.size(); i++) {
        vec[i] -= v[i];
    }
    return *this;
}

SSTP::Vector& SSTP::Vector::operator*=(double x)
{
    for (size_t i = 0; i < vec.size(); i++) {
        vec[i] *= x;
    }
    return *this;
}

SSTP::Vector& SSTP::Vector::operator/=(double x)
{
    for (size_t i = 0; i < vec.size(); i++) {
        vec[i] /= x;
    }
    return *this;
}

SSTP::Vector& SSTP::Vector::operator=(const Vector& v)
{
    if (v.dim == dim) {
        std::copy(v.vec.begin(), v.vec.end(), vec.begin());
    }
    else {
        vec = v.vec;
        dim = v.dim;
    }
    return *this;
}

SSTP::Vector SSTP::Vector::operator+(double x) const
{
    Vector result{*this};
    result += x;
    return result;
}

SSTP::Vector SSTP::Vector::operator+(const Vector& v) const
{
    Vector result{*this};
    result += v;
    return result;
}

SSTP::Vector SSTP::Vector::operator-(double x) const
{
    Vector result{*this};
    result -= x;
    return result;
}

SSTP::Vector SSTP::Vector::operator-(const Vector& v) const
{
    Vector result{*this};
    result -= v;
    return result;
}

SSTP::Vector SSTP::Vector::operator*(double x) const
{
    Vector result{*this};
    result *= x;
    return result;
}

double SSTP::Vector::operator*(const Vector& v) const
{
    if (v.dim != dim) {
        throw std::out_of_range(
            "Tried to multiply vectors of different size (" + std::to_string(dim) + " != " + std::to_string(v.dim) + ")"
        );
    }
    return std::inner_product(vec.begin(), vec.end(), v.vec.begin(), 0.0);
}

SSTP::Vector SSTP::Vector::operator/(double x) const
{
    Vector result{*this};
    result /= x;
    return result;
}

namespace SSTP {
    std::ostream &operator<<(std::ostream &os, const Vector& v)
    {
        os << "[";
        for (size_t i = 0; i < v.vec.size(); i++) {
            os << v.vec[i];
            if (i != v.vec.size() - 1) {
                os << ", ";
            }
        }
        os << "]";
        return os;
    }

    Vector operator+(double x, const Vector& v)
    {
        return v + x;
    }

    Vector operator-(double x, const Vector& v)
    {
        return v - x;
    }

    Vector operator*(double x, const Vector& v)
    {
        return v * x;
    }
}