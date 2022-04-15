#include <iostream>
#include <random>
#include <cmath>
#include <ctime>
#include <time.h>
using namespace std;

// problem: this random generator does not work!!!

class Vanilla_Call{
    public:
        double S0;
        double R;
        double K;
        double T;
        double Sigma;

        Vanilla_Call(){
            S0 = 0;
            R = 0;
            K = 0;
            T = 0;
            Sigma = 0;
            cout<<"insufficient input!"<<endl;
        }
        Vanilla_Call(double s0, double r, double k, double t, double sigma){
            S0 = s0;
            R = r;
            K = k;
            T = t;
            Sigma = sigma;
        } 
        double price(){
            int path = 1000000;
            double summation_of_simulated_call = 0.0;
            default_random_engine generator((unsigned)time(NULL));
            normal_distribution<double> distribution(0.0,1.0);
            
            for(int i=1; i <= path; i++){
                double normalRandom = distribution(generator);
                double log_ST = (log(S0) + (R - Sigma * Sigma * 0.5) * T) + Sigma*sqrt(T)*normalRandom;  
                double ST = exp(log_ST);
                double simulated_call = max<double>(ST-K, 0);
                summation_of_simulated_call += simulated_call;
            }

            double average_of_simulated_call = summation_of_simulated_call / path;
            double discounted_call_price = exp(-1*R*T) * average_of_simulated_call;
            return(discounted_call_price);
        }
};

class Vanilla_Put{
    public:
        double S0;
        double R;
        double K;
        double T;
        double Sigma;

        Vanilla_Put(){
            S0 = 0;
            R = 0;
            K = 0;
            T = 0;
            Sigma = 0;
            cout<<"insufficient input!"<<endl;
        }
        Vanilla_Put(double s0, double r, double k, double t, double sigma){
            S0 = s0;
            R = r;
            K = k;
            T = t;
            Sigma = sigma;
        } 
        double price(){
            int path = 1000000;
            double summation_of_simulated_put = 0.0;
            default_random_engine generator((unsigned)time(NULL));
            normal_distribution<double> distribution(0.0,1.0);
            
            for(int i=1; i <= path; i++){
                double normalRandom = distribution(generator);
                double log_ST = (log(S0) + (R - Sigma * Sigma * 0.5) * T) + Sigma*sqrt(T)*normalRandom;  
                double ST = exp(log_ST);
                double simulated_put = max<double>(K-ST, 0);
                summation_of_simulated_put += simulated_put;
            }

            double average_of_simulated_put = summation_of_simulated_put / path;
            double discounted_put_price = exp(-1*R*T) * average_of_simulated_put;
            return(discounted_put_price);
        }
};
