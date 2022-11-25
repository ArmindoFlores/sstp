#ifndef _VECTOR_H_
#define _VECTOR_H_

#include <iostream>
#include <vector>

namespace SSTP {
    /*
    This class is used to describe an N-dimensional vector
    */
    class Vector {
    public:
        Vector(std::size_t N);
        Vector(const double* arr, std::size_t N);
        Vector(const std::vector<double>& vec);
        Vector(const Vector& vec);
        Vector(Vector&& vec);

        double& operator[](std::size_t i);
        double operator[](std::size_t i) const;

        Vector& operator+=(double x);
        Vector& operator+=(const Vector& v);
        Vector& operator-=(double x);
        Vector& operator-=(const Vector& v);
        Vector& operator*=(double x);
        Vector& operator/=(double x);
        Vector& operator=(const Vector& v);
        Vector operator+(double x) const;
        Vector operator+(const Vector& v) const;
        Vector operator-(double x) const;
        Vector operator-(const Vector& v) const;
        Vector operator*(double x) const;
        double operator*(const Vector& v) const;
        Vector operator/(double x) const;

        std::size_t dimension() const;
        double length() const;
        Vector normalized() const;

        friend std::ostream &operator<<(std::ostream &os, const Vector& v);

        friend Vector operator+(double x, const Vector& v);
        friend Vector operator-(double x, const Vector& v);
        friend Vector operator*(double x, const Vector& v);

    private:
        std::vector<double> vec;
        std::size_t dim;
    };
}

#endif