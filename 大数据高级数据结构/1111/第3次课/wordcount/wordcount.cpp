#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mapreduce.h"

using namespace std;

void Map(char *file_name) {
    FILE *fp = fopen(file_name, "r");
    char line[1024];
    printf("filename is [%s] \n",file_name);
    assert(fp != NULL);
    while (fgets(line, 1024, fp) != NULL) {
        char *token, *dummy = line;
        for (token = strtok(dummy, " \t\n\r");token!= NULL;token=strtok(NULL," \t\n\r")) {
            MR_Emit(token, "1");
        }
    }
    fclose(fp);
}

void Reduce(char *key, Getter get_next, int partition_number) {
    int count = 0;
    char *value;
    while ((value = get_next(key, partition_number)) != NULL)
        count++;
    printf("partition_number=%d key=%s count=%d\n", partition_number,key, count);
}

int main(int argc, char *argv[]) {
    MR_Run(argc, argv, Map, 4, Reduce, 10, MR_DefaultHashPartition);
}
