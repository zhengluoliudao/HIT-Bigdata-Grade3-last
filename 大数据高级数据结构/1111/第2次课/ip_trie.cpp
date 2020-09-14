#include <iostream>
using namespace std;
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
//#include <sys/socket.h>
//#include <arpa/inet.h>
#include <stdio.h>

const int maxn =1000;//如果是64MB可以开到2e6+5，尽量开大
int  tree[maxn][256];//tree[i][j]表示节点i的第j个儿子的节点编号
bool flagg[maxn];//表示以该节点结尾是一个单词
int  tot;//总节点数

void insert(char *str)
{
   int  len=strlen(str);
   int root=0;
   for(int i=0;i<len;i++)
   {
       int id=str[i]-'0';
       if(!tree[root][id]) tree[root][id]=++tot;
       root=tree[root][id];
   }
   flagg[root]=true;
}
bool find(char *str)//查询操作，按具体要求改动
{
    int len=strlen(str);
    int root=0;
    for(int i=0;i<len;i++)
    {
        int id=str[i]-'0';
        if(!tree[root][id]) return false;
        root=tree[root][id];
    }
    return true;
}

void init()//最后清空，节省时间
{
    for(int i=0;i<=tot;i++)
    {
       flagg[i]=false;
       for(int j=0;j<10;j++)
           tree[i][j]=0;
    }
   tot=0;//RE有可能是这里的问题
}

char    ready_mask[30];
//函数将点分十进制IP如234.234.23.2/34 转化为一系列IP地址然后再插入字典树
char IPdotdec[20]; //存放点分十进制IP地址
//struct in_addr s; // IPv4地址结构体
//struct in_addr   in;
void   pre_start(char  *str)
{
   char  *delim = "/";
   char   *tokenPtr =strtok(str,delim);
   int  i=0;
   while(tokenPtr!=NULL&&i < 1)
   {
       cout<<tokenPtr<<endl;
       strcpy(IPdotdec,tokenPtr);
       tokenPtr=strtok(NULL,delim);
       i++;
       strcpy(ready_mask,tokenPtr);
   }

 /*由于windows下未装网络相关库#include <sys/socket.h> #include <arpa/inet.h>，为了顺利进行编译因而注释，后续需要演示带掩码的进行加入。
    int  aa=inet_addr(IPdotdec);  //将一个IPV4地址的字符串转换成一个无符号整数函数：
    printf(" ip_int 0x%x\n",aa);
    int   l=  htonl(aa);
    printf("aa : 0x%x\n",l);
    printf("aa : %d\n",l);

    int num_int = atoi(read_mask);          //转换为整型值

    if(num_int==24)
    {

    }
    else if(num_int==25)
    {

    }
    else if((num_int==26)
    {
    }
    .....
   */
}


/*
  这是精确匹配
   譬如
       带匹配IP地址为  192.168.45.3

   而模式库IP为：
           192.168.45.3/32
           182.168.45.2/32
           34.45.23.5/32
           34.34.24.33/32
   默认掩码位数为32
   如果出现掩码位数为小于32的（前提大于24），我们需要将其模式进行预处理，转化为一个个IP地址
   如下：
       192.168.45.3/31
       我们将其转化为：
       192.168.45.2/32     192.168.45.3/32    两个IP然后对转化后的IP进行构建字典树



*/
char   s[30][100];
int   main()
{
    int n;
    cin>>n;

    for(int i=0;i<n;i++)
    {
        cin>>s[i];
        insert(s[i]);
    }

    char  test[30];
    cin>>test;
    cout<<find(test)<<endl;
    return   0;
}
