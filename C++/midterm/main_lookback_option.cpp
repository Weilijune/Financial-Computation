#include <iostream>
#include <cmath>
#include <vector>
#include "lookback_option.h"
using namespace std;

// main function
int main(int argc, char const *argv[])
{
    // input
    double S0, r, q, sigma, T; 
    int n ;
    cout<<"enter Stock price at t = 0: ";
    cin>>S0;
    cout<<"enter r (riskfree rate): ";
    cin>>r;
    cout<<"enter q (dividend rate): ";
    cin>>q;
    cout<<"enter sigma (volatility): ";
    cin>>sigma;
    cout<<"enter T (maturity): ";
    cin>>T;
    cout<<"enter time steps (at most 100): "; // n at most 100 steps
    cin>>n;

    Lookback_Option lookback_option(S0, r, q, T, sigma, n);

    // output
    cout<<"Tree model: "<<endl;
    cout<<"  European Lookback call price = "<<lookback_option.eur_call_price()<<endl;
    cout<<"  European Lookback put  price = "<<lookback_option.eur_put_price()<<endl;
    cout<<"  American Lookback call price = "<<lookback_option.am_call_price()<<endl;
    cout<<"  American Lookback put  price = "<<lookback_option.am_put_price()<<endl;

    return 0;
}
