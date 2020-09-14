#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>
using namespace std;
#include "bloom_filter.hpp"
void readfile2(bloom_filter &filter)
{
    ifstream file2("file2.txt");
    string line;
    while (getline(file2, line))
    {
        filter.insert(line);
    }
    cout << "file2 contains " << filter.element_count() << " urls." << endl;
    return;
}
void test(bloom_filter &filter)
{
    ifstream file1("file1.txt");
    ofstream outfile("count.txt");
    string line;
    int count = 0;
    while (getline(file1, line))
    {
        if (filter.contains(line))
        {
            outfile << line << endl;
        }
    }
    outfile.close();
}
int main()
{

    bloom_parameters parameters;
    parameters.projected_element_count = 470000;
    parameters.false_positive_probability = 0.001;
    parameters.random_seed = 0xC7C7C7C7;
    if (!parameters)
    {
        cout << "Error - Invalid set of bloom filter parameters!" << endl;
        return 1;
    }
    parameters.compute_optimal_parameters();
    bloom_filter filter(parameters);
    readfile2(filter);
    test(filter);
    system("pause"); 
}