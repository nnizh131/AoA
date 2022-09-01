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

// struct TreeNode get_node(char *line){
//     struct TreeNode node;
//     node.column = strtol(strtok(line,","), NULL, 10);
//     node.threshold = strtof(strtok(NULL,","), NULL);
//     node.left_child = strtol(strtok(NULL,","), NULL, 10);
//     node.right_child = strtol(strtok(NULL,","), NULL, 10);
//     node.value = strtof(strtok(NULL,","), NULL);
//     return node;
// };


float predict(char *argv[]){
    int ntrees;
    int nrows;
    long int current_node;
    float prediction_sum = 0;
    FILE *binary_file = fopen("forest.bin", "rb");
    fread(&ntrees, sizeof(int), 1, binary_file);

    printf("ntrees %d\n", ntrees);

    int i;
    int j;
    float predictors[10];
    for(i=0; i<10; i++){
        predictors[i] = strtof(argv[i], NULL);
        printf("%f\n", predictors[i]);
    };

    long int column;
    float value;
    float threshold;
    for(i=0; i<ntrees; i++){
        fread(&nrows, sizeof(int), 1, binary_file);
        struct TreeNode tree[nrows];
        fread(tree, sizeof(struct TreeNode)*nrows, 1, binary_file);
        
        // work through the 
        current_node = 0;
        while(tree[current_node].column > -1){
            value = predictors[tree[current_node].column];
            threshold = tree[current_node].threshold;
            current_node = value < threshold ? tree[current_node].left_child : tree[current_node].right_child;
        };
        prediction_sum = prediction_sum + tree[current_node].value;
    };
    return(prediction_sum/ntrees);
};

void main(){
    float prediction;
    // int argc = 1;
    char *argv[] = {"-0.251084","0.011985","-0.004184","0.011310","-0.009187","-0.007796","0.011729","0.002421","0.011187","0.004386"};
    prediction = predict(argv);
    printf("Prediction: %f\n", prediction);
}