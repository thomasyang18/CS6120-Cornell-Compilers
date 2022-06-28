#include <stdio.h>

int main(){
	int t; scanf("%d\n", &t);
	while(t--){
		int n; scanf("%d\n", &n);
		int a = 100000000;
		int sum = 0;
		for(int i = 0; i < n; i++){
			int j; scanf("%d\n", &j);
			sum += j;
			if (j <= a) a = j;
		}
		printf("%d\n", sum-a*n);
	}
}
