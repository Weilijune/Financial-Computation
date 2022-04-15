#include <iostream>
#include <cmath>
using namespace std;
double stdNormalCdf(double x){
    return erfc(-x/sqrt(2))/2; // erro function
}
int main(int argc, char const *argv[])
{
    double s, r, q, k, sigma, t;
    s = 50;
    r = 0.1;
    q = 0;
    k = 50;
    sigma = 0.25;
    t = 1;
    
    double d1 = (log(s * exp(-q*t)) - log(k * exp(-r*t)))/(sigma*sqrt(t)) + 0.5*sigma*sqrt(t);
    double d2 = d1 - sigma*sqrt(t);
    double call = s * exp(-q*t) * stdNormalCdf(d1) - k * exp(-r*t) * stdNormalCdf(d2);
    cout<<call<<endl;
    return 0;
}
