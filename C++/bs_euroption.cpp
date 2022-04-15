#include <iostream>
#include <cmath>
#include "Euroption.h"
using namespace std;

//with or without parameters
Euroption::Euroption(){s = 0; r = 0; q = 0; t = 0; sigma = 0; k = 0; type= 'c';};
Euroption::Euroption(double as, double ar, double aq, double at, double asigma, double ak, char atype){
    s = as;
    r = ar;
    q = aq;
    t = at;
    sigma = asigma;
    k = ak;
    type = atype;
}
// getter
double Euroption::get_s() const {return s; };
double Euroption::get_r() const {return r; };
double Euroption::get_q() const {return q; };
double Euroption::get_t() const {return t; };
double Euroption::get_sigma() const {return sigma; };
double Euroption::get_k() const {return k; };
char Euroption::get_type() const {return type; };

// setter
void Euroption::set_s(double as) {Euroption::s = as;};
void Euroption::set_r(double ar) {Euroption::r = ar;};
void Euroption::set_q(double aq) {Euroption::q = aq;};
void Euroption::set_t(double at) {Euroption::t = at;};
void Euroption::set_sigma(double asigma) {Euroption::sigma = asigma;};
void Euroption::set_k(double ak) {Euroption::k = ak;};
void Euroption::set_type(char atype) {Euroption::type = atype;};

// standard normal cdf
double stdNormalCdf(double x){
    return erfc(-x/sqrt(2))/2; // erro function
}

//call price
double Euroption::eurcall() const{
    double d1 = (log(s * exp(-q*t)) - log(k * exp(-r*t)))/(sigma*sqrt(t)) + 0.5*sigma*sqrt(t);
    double d2 = d1 - sigma*sqrt(t);
    double call = s * exp(-q*t) * stdNormalCdf(d1) - k * exp(-r*t) * stdNormalCdf(d2);
    return call;
}

//put price
double Euroption::eurput() const{
    double d1 = (log(s * exp(-q*t)) - log(k * exp(-r*t)))/(sigma*sqrt(t)) + 0.5*sigma*sqrt(t);
    double d2 = d1 - sigma*sqrt(t);
    double put = k * exp(-r*t) * stdNormalCdf(-d2) - s * exp(-q*t) * stdNormalCdf(-d1);
    return put;
}

//option price
double Euroption::eurprice() const{
    if(type == 'c'){
        double price = Euroption::eurcall();
        return price;
    }
    else{
        double price = Euroption::eurput();
        return price;
    }
}

// main function
int main(int argc, char const *argv[])
{
    Euroption option1(50,0.1,0,1,0.25,50,'c');
    cout<<option1.eurprice()<<endl;
    return 0;
}
