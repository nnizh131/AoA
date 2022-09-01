#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct TreeNode{
    long int column;
    float threshold;
    long int left_child;
    long int right_child;
    float value;
};

struct TreeNode get_node(char *line){
    struct TreeNode node;
    node.column = strtol(strtok(line,","), NULL, 10);
    node.threshold = strtof(strtok(NULL,","), NULL);
    node.left_child = strtol(strtok(NULL,","), NULL, 10);
    node.right_child = strtol(strtok(NULL,","), NULL, 10);
    node.value = strtof(strtok(NULL,","), NULL);
    return node;
};

void main1(){
    int argc = 2;
    char *argv[] = {"tree0.csv"};
    char line[512];
    char * token;
    int nrows;
    int ntrees = 1;
    FILE *binary_file = fopen("forest.bin", "wb");
    struct TreeNode node;
    
    int i;
    int j;
    
    fwrite(&ntrees, sizeof(int), 1, binary_file);
    for(i=0; i<ntrees; i++){
        j=0;
        printf("%d", i);
        FILE *f = fopen(argv[i], "r");
        printf("%s", argv[i]);
        nrows = atoi(fgets(line, 512, f));
        struct TreeNode tree[nrows];
        fwrite(&nrows, sizeof(int), 1, binary_file);
        while(fgets(line, 512, f)){
            tree[j] = get_node(line);
            printf("%f\n", tree[j].value);
            j++;
        };
        fwrite(tree, sizeof(struct TreeNode)*nrows, 1, binary_file);
        fclose(f);
    };
    fclose(binary_file);
}