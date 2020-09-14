#include <iostream>
using namespace std;
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
//#include <sys/socket.h>
//#include <arpa/inet.h>
#include <stdio.h>

const int maxn =1000;//�����64MB���Կ���2e6+5����������
int  tree[maxn][256];//tree[i][j]��ʾ�ڵ�i�ĵ�j�����ӵĽڵ���
bool flagg[maxn];//��ʾ�Ըýڵ��β��һ������
int  tot;//�ܽڵ���

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
bool find(char *str)//��ѯ������������Ҫ��Ķ�
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

void init()//�����գ���ʡʱ��
{
    for(int i=0;i<=tot;i++)
    {
       flagg[i]=false;
       for(int j=0;j<10;j++)
           tree[i][j]=0;
    }
   tot=0;//RE�п��������������
}

char    ready_mask[30];
//���������ʮ����IP��234.234.23.2/34 ת��Ϊһϵ��IP��ַȻ���ٲ����ֵ���
char IPdotdec[20]; //��ŵ��ʮ����IP��ַ
//struct in_addr s; // IPv4��ַ�ṹ��
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

 /*����windows��δװ������ؿ�#include <sys/socket.h> #include <arpa/inet.h>��Ϊ��˳�����б������ע�ͣ�������Ҫ��ʾ������Ľ��м��롣
    int  aa=inet_addr(IPdotdec);  //��һ��IPV4��ַ���ַ���ת����һ���޷�������������
    printf(" ip_int 0x%x\n",aa);
    int   l=  htonl(aa);
    printf("aa : 0x%x\n",l);
    printf("aa : %d\n",l);

    int num_int = atoi(read_mask);          //ת��Ϊ����ֵ

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
  ���Ǿ�ȷƥ��
   Ʃ��
       ��ƥ��IP��ַΪ  192.168.45.3

   ��ģʽ��IPΪ��
           192.168.45.3/32
           182.168.45.2/32
           34.45.23.5/32
           34.34.24.33/32
   Ĭ������λ��Ϊ32
   �����������λ��ΪС��32�ģ�ǰ�����24����������Ҫ����ģʽ����Ԥ����ת��Ϊһ����IP��ַ
   ���£�
       192.168.45.3/31
       ���ǽ���ת��Ϊ��
       192.168.45.2/32     192.168.45.3/32    ����IPȻ���ת�����IP���й����ֵ���



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
