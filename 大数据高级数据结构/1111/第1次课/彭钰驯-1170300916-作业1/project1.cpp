#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;
#include "bitmap.hpp"
#include "bloom_filter.hpp"

int a[10000];
int rand_max = 20000;

int main()
{
    srand((unsigned)time(NULL));
    for (int i = 0; i < 10000; i++)
    {
        a[i] = rand() % rand_max;
    }
    bloom_parameters parameters;
    parameters.projected_element_count = 10000;
    parameters.false_positive_probability = 0.001;
    parameters.random_seed = 0xC7C7C7C7;
    if (!parameters)
    {
        cout << "Error - Invalid set of bloom filter parameters!" << endl;
        return 1;
    }
    parameters.compute_optimal_parameters();
    bloom_filter filter(parameters);
    BitMap bitmap(0, rand_max);
    for (int i = 0; i < 10000; i++)
    {
        bitmap.set(a[i]);
        filter.insert(a[i]);
    }
    int wrong = 0;
    for (int i = 0; i < 1000; i++)
    {
        int tmp = rand() % rand_max;
        int flag_bit = 0, flag_bloom = 0;
        if (bitmap.test(tmp))
        {
            flag_bit = 1;
        }
        if (filter.contains(tmp))
        {
            flag_bloom = 1;
        }
        if (flag_bit != flag_bloom)
        {
            wrong++;
        }
    }
    cout << "wrong rate:" << double(wrong) / 1000.0 << endl;
    system("pause"); 
}