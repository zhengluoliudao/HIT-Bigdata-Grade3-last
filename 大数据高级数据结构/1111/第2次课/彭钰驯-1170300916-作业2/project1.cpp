#include "tire.h"
#include <iostream>
#include <fstream>
#include <string>
void init(node &root)
{
    std::ifstream wordlist("wordlist1.txt");
    std::string line;
    while(getline(wordlist, line))
    {
        root.insert(line);
    }
}
int main()
{
    node T;
    init(T);
    while(1)
    {
        std::string op;
        std::cin >> op;
        if(op=="q")
        {
            return 0;
        }
        else
        {
            if(T.find(op))
            {
                std::cout << "exist" << std::endl;
            }
            else
            {
                std::cout << "not exist" << std::endl;
            }
        }
    }
}
