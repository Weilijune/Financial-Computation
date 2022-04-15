#include <iostream>
#include <random>
#include <cmath>
#include <ctime>
#include <time.h>
using namespace std;

class Asian_Call{
    public:
        double S0;
        double R;
        double T;
        double Sigma;

        Asian_Call(){
            S0 = 0;
            R = 0;
            T = 0;
            Sigma = 0;
            cout<<"insufficient input!"<<endl;
        }
        Asian_Call(double s0, double r, double t, double sigma){
            S0 = s0;
            R = r;
            T = t;
            Sigma = sigma;
        }

        double price(){
            int n = 100;
            int path = 20;
            double delta_t = T / n;
            double sum_of_payoff = 0.0;

            default_random_engine generator((unsigned)time(NULL));
            normal_distribution<double> distribution(0.0,1.0);
            
            for(int i = 1; i <= path; i++){
                double S = S0;
                double sum_of_s = 0.0;

                for(int i=1; i <= n; i++){
                    double normalRandom = distribution(generator);
                    double log_S = (log(S) + (R - Sigma * Sigma * 0.5) * delta_t) + Sigma*sqrt(delta_t)*normalRandom;  
                    S = exp(log_S);
                    sum_of_s += S;
                }
                
                double s_ave = sum_of_s / n;
                double payoff = max<double>(S - s_ave, 0);
                sum_of_payoff += payoff;
            }
            
            double average_payoff = sum_of_payoff / path;
            
            double discounted_price = average_payoff * exp(-1 * R * T);
            return(discounted_price);
        }
};

class Asian_Put{
    public:
        double S0;
        double R;
        double T;
        double Sigma;

        Asian_Put(){
            S0 = 0;
            R = 0;
            T = 0;
            Sigma = 0;
            cout<<"insufficient input!"<<endl;
        }
        Asian_Put(double s0, double r, double t, double sigma){
            S0 = s0;
            R = r;
            T = t;
            Sigma = sigma;
        }

        double price(){
            int n = 100;
            int path = 20;
            double delta_t = T / n;
            double sum_of_payoff = 0.0;


            default_random_engine generator((unsigned)time(NULL));
            normal_distribution<double> distribution(0.0,1.0);
            
            for(int i = 1; i <= path; i++){
                double S = S0;
                double sum_of_s = 0.0;
                for(int i=1; i <= n; i++){
                    double normalRandom = distribution(generator);
                    double log_S = (log(S) + (R - Sigma * Sigma * 0.5) * delta_t) + Sigma*sqrt(delta_t)*normalRandom;  
                    S = exp(log_S);
                    sum_of_s += S;
                }
                
                double s_ave = sum_of_s / n;
                double payoff = max<double>(s_ave - S, 0);
                sum_of_payoff += payoff;
                
            }
            
            double average_payoff = sum_of_payoff / path;
            double discounted_price = average_payoff * exp(-1 * R * T);
            return(discounted_price);
        }
};
