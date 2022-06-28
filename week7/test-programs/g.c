#include<stdlib.h>
#include<stdio.h>

int n;
int *adj[4010];
int size[4010];
int true_size[4010];
char s[4010];


void init(){
	for (int i = 0; i < n; i++) {
		size[i] = 0;
		true_size[i] = 10;
		adj[i] = malloc(sizeof(int) * true_size[i]); 
	} 
}

void add_edge(int i, int j){
	adj[i][size[i]++] = j;
	
	if (size[i] == true_size[i]-1){
		true_size[i]*=2;
		adj[i] = realloc(adj[i], sizeof(int) * true_size[i]);
	}
}

void clear(){
	for (int i = 0; i < n; i++) free(adj[i]);
}
int cost;

int solve(int a){
	
	int bal = s[a] == 'W' ? 1:-1;
	for (int i = 0; i < size[a]; i++){
		bal += solve(adj[a][i]);
	}
	if (bal == 0) cost++;
	return bal;
}

int main(){
	int t;
	scanf("%d\n", &t);
	while(t--){
		scanf("%d\n", &n);
		init();
		for (int i = 0; i < n-1; i++){
			int cur;
			if (i == n-2) scanf("%d\n", &cur);
			else scanf("%d ", &cur);
			add_edge(cur-1, i+1);
		}
		scanf("%s\n", s);
		
		cost = 0;
		solve(0);
		printf("%d\n", cost);
		clear();
	}
}
