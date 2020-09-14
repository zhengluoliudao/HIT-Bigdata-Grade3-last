#include "tire.h"
#include <iostream>
#include <fstream>
#include <string>
void init(node &root)
{
    std::ifstream file("article1.txt");
    std::string str;
    while (file >> str)
    {
        root.insert(str);
    }
}
void show(node *root, std::string now)
{
    for (int i = 0; i < 26; i++)
    {
        if (root->next[i] == NULL)
            continue;
        if (root->next[i]->isStr)
        {
            std::cout << now + (std::string(1, char('a' + i))) << " " << root->next[i]->count << std::endl;
        }
        show(root->next[i], now + (std::string(1, char('a' + i))));
    }
}
int main()
{
    node T;
    init(T);
    show(&T, "");
    getchar();
}