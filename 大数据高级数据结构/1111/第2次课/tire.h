#include <string>
struct node
{
    node *next[26];
    bool isStr;
    int count = 0;
    node()
    {
        for (int i = 0; i < 26; i++)
        {
            next[i] = NULL;
        }
    }
    void insert(std::string s)
    {
        node *p = this;
        for (int i = 0; i < s.size(); i++)
        {
            if (p->next[s[i] - 'a'] == NULL)
            {
                node *temp = new node;
                temp->isStr = false;
                p->next[s[i] - 'a'] = temp;
            }
            p = p->next[s[i] - 'a'];
        }
        p->isStr = true;
        p->count++;
    }
    bool find(std::string s)
    {
        node *p = this;
        for (int i = 0; i < s.size(); i++)
        {
            if (p->next[s[i] - 'a'] == NULL)
            {
                return false;
            }
            else
            {
                p = p->next[s[i] - 'a'];
            }
        }
        if (p->isStr)
            return true;
        else
            return false;
    }
    bool remove(std::string s)
    {
        node *p = this;
        for (int i = 0; i < s.size(); i++)
        {
            if (p->next[s[i] - 'a'] == NULL)
            {
                return false;
            }
            else
            {
                p = p->next[s[i] - 'a'];
            }
        }
        if (p->isStr)
        {
            p->isStr = false;
            p->count = 0;
            return true;
        }
        else
        {
            return false;
        }
    }
};