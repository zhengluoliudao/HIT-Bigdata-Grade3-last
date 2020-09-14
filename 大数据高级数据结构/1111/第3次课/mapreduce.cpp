#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "mapreduce.h"
#include <string.h>

pthread_mutex_t file_lock;
char** file_list;
Partitioner partitioner; Mapper mapper; Reducer reducer;
int REDUCERS_NUM, FILES_NUM, files_counter;
typedef struct value_node{
    char* value;
    struct value_node* next;
} v;
typedef struct key_node{
    v* head;//Corresponding value
    char* key;
    struct key_node* next;
} k;
struct key_entry {
    k* head;
    pthread_mutex_t lock;
};
struct partition_entry{
    pthread_mutex_t lock;
    int num_keys;//number of keys in linklist
    int curr_ptr;//current ptr for traversal purposes
    k* sorted_keys;//sorted_keys in ascending key order (alphabetical)
    struct key_entry list[1024];
};
struct partition_entry hash_map[128];
int str_comparator(const void* a, const void* b){
    return strcmp(((k*)a)->key, ((k*)b)->key);
}
char* get_next(char *key, int partition_number){
    char* value = NULL;
    k* keys_list = hash_map[partition_number].sorted_keys;
    for(value = NULL;;){
        int curr = hash_map[partition_number].curr_ptr;
        if (strcmp(keys_list[curr].key, key) == 0){
            if (keys_list[curr].head == NULL) return NULL;
            v* temp = keys_list[curr].head->next;
            value = keys_list[curr].head->value, keys_list[curr].head = temp;
            return value;
        } else {
            hash_map[partition_number].curr_ptr++;
            continue;
        }
        return NULL;
    }
}
void* threads_mapper(void* arg){
    char* filename = NULL;
    for (filename = NULL;;){
        pthread_mutex_lock(&file_lock);
        if(files_counter >= FILES_NUM){
            pthread_mutex_unlock(&file_lock);
            return NULL;
        }
        filename = file_list[files_counter++];
        pthread_mutex_unlock(&file_lock);
        (*mapper)(filename);//CALL OPEN FUNC
    }
}
void* threads_reducer(void* arg){
    int partition_number = *(int*)arg;
    int i = 0,ptr=0;
    free(arg);arg = NULL;
    if(hash_map[partition_number].num_keys == 0) return NULL;
    hash_map[partition_number].sorted_keys = (k*)malloc(sizeof(k) * hash_map[partition_number].num_keys);
    for (i = 0,ptr = 0; i < 1024; i++){
        k* curr_k = hash_map[partition_number].list[i].head;
        if (curr_k == NULL) continue;
        while (curr_k != NULL){
            hash_map[partition_number].sorted_keys[ptr] = *curr_k, curr_k = curr_k -> next;
            ptr++;//put curr_k at approperiate position in sorted list
        }
    }
    qsort(hash_map[partition_number].sorted_keys, hash_map[partition_number].num_keys, sizeof(k), str_comparator);
    for (i = 0; i < hash_map[partition_number].num_keys; i++){
        (*reducer)(hash_map[partition_number].sorted_keys[i].key, get_next ,partition_number);//call reducer function sequentially
    }
    //Clean up
    for (i = 0; i < 1024; i++){
        k* curr_k = hash_map[partition_number].list[i].head;
        if (curr_k == NULL) continue;//skip null
        while (curr_k != NULL){//free everything on the way
            free(curr_k->key);
            curr_k->key = NULL;
            v* curr_v = curr_k->head;//free corresponding value node
            while (curr_v != NULL){
                free(curr_v->value);
                curr_v->value = NULL;
                v* temp_v = curr_v -> next;
                free(curr_v);
                curr_v = temp_v;
            }
            curr_v = NULL;
            k* temp_k = curr_k -> next;
            free(curr_k);
            curr_k = temp_k;
        }
        curr_k = NULL;
    }
    free(hash_map[partition_number].sorted_keys);
    hash_map[partition_number].sorted_keys = NULL;
    return NULL;
}
unsigned long MR_DefaultHashPartition(char *key, int num_partitions){
    unsigned long hash = 5381;
    int c;
    while ((c = *key++) != '\0')
        hash = hash * 33 + c;
    return hash % num_partitions;
}
void MR_Emit(char *key, char *value){
    unsigned long partition_number = (*partitioner)(key, REDUCERS_NUM), map_number = MR_DefaultHashPartition(key, 1024);
    pthread_mutex_lock(&hash_map[partition_number].list[map_number].lock);
    k* temp = hash_map[partition_number].list[map_number].head;
    for(;temp != NULL;temp = temp->next){
        if (strcmp(temp->key, key) == 0) break;
    }
    v* vnode = (v*)malloc(sizeof(v));
    if (vnode == NULL) {
        perror("malloc failed @ Emit");
        pthread_mutex_unlock(&hash_map[partition_number].list[map_number].lock);
        return;
    }
    vnode->value = (char*)malloc(sizeof(char)*20);
    strcpy(vnode->value, value);
    vnode->next = NULL;
    if (temp == NULL){    //no existing node for same key
        k *knode = (k*)malloc(sizeof(k));
        if (knode == NULL) {
            perror("malloc failed @ Emit");
            pthread_mutex_unlock(&hash_map[partition_number].list[map_number].lock);
            return;
        }
        knode->head = vnode, knode->next = hash_map[partition_number].list[map_number].head, knode->key = (char*)malloc(sizeof(char)*20), hash_map[partition_number].list[map_number].head = knode;
        strcpy(knode->key, key);
        pthread_mutex_lock(&hash_map[partition_number].lock);
        hash_map[partition_number].num_keys++;
        pthread_mutex_unlock(&hash_map[partition_number].lock);
    } else {
        vnode->next = temp->head, temp->head = vnode;
    }
    pthread_mutex_unlock(&hash_map[partition_number].list[map_number].lock);
}
void MR_Run(int argc, char *argv[],
        Mapper map, int num_mappers,
        Reducer reduce, int REDUCERS_NUMs,
        Partitioner partition){
    //initialization
    int i=0,j=0;
    pthread_mutex_init(&file_lock, NULL);
    file_list = (argv + 1), partitioner = partition, mapper = map, reducer = reduce;
    REDUCERS_NUM = REDUCERS_NUMs, FILES_NUM = argc - 1, files_counter = 0;
    for (i = 0;i < REDUCERS_NUM; i++){
        pthread_mutex_init(&hash_map[i].lock, NULL);//give each entry a lock
        hash_map[i].num_keys = 0, hash_map[i].curr_ptr = 0, hash_map[i].sorted_keys = NULL;
        for (j = 0; j < 1024; j++){
            hash_map[i].list[j].head = NULL;
            pthread_mutex_init(&hash_map[i].list[j].lock, NULL);
        }
    }
    pthread_t threads_mappers[num_mappers];//create map threads
    for (i = 0; i < num_mappers; i++){
        pthread_create(&threads_mappers[i], NULL, threads_mapper, NULL);
    }
    for (i = 0; i < num_mappers; i++){//wait for map threads
        pthread_join(threads_mappers[i], NULL);
    }
    pthread_t threads_reducers[REDUCERS_NUMs];//create reduce threads
    for (i = 0; i < REDUCERS_NUMs; i++){
        void* arg = malloc(4);
        *(int*)arg = i;
        pthread_create(&threads_reducers[i], NULL, threads_reducer, arg);
    }
    for (i = 0; i < REDUCERS_NUMs; i++){//wait for reduce threads
        pthread_join(threads_reducers[i], NULL);
    }
}


