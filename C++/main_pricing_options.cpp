#include <iostream>
using namespace std;

#include "plain_vanilla.h"
#include "asian_option.h"
int main(int argc, char const *argv[])
{
    Vanilla_Call call1(50, 0.1, 50, 1, 0.25);
    cout<<call1.price()<<endl;
    
    Vanilla_Put put1(50, 0.1, 50, 1, 0.25);
    cout<<put1.price()<<endl;

    Asian_Call call2(50, 0.1, 1, 0.25);
    cout<<call2.price()<<endl;
    
    Asian_Put put2(50, 0.1, 1, 0.25);
    cout<<put2.price()<<endl;

    return 0;
}


