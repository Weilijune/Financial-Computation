#include <iostream>
#include <cmath>
using namespace std;
class Euroption{
    private:
        double s;
        double r;
        double q;
        double t;
        double sigma;
        double k;
        char type;

    public:
        Euroption();
        Euroption(double s, double r, double q, double t, double sigma, double k, char type);
        // getter
        double get_s() const;
        double get_r() const;
        double get_q() const;
        double get_t() const;
        double get_sigma() const;
        double get_k() const;
        char get_type() const;

        // setter
        void set_s(double as);
        void set_r(double ar);
        void set_q(double aq);
        void set_t(double at);
        void set_sigma(double asigma);
        void set_k(double ak);
        void set_type(char atype);
    private:
        double eurcall() const;
        double eurput() const;
    public:
        double eurprice() const;
};
