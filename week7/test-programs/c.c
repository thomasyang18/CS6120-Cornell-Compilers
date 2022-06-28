#include<string.h>
#include<stdlib.h>
#include<stdio.h>

char strings[60][10];

int main(){
	int t; scanf("%d\n", &t);
	while(t--){
		int n, m; scanf("%d %d\n", &n, &m);
		for (int i = 0; i < n; i++){
			scanf("%s\n", strings[i]);
		}
		int ans = 209239324;
		for (int i = 0; i < n; i++){
			for (int j = i+1; j < n; j++){
				int tans = 0;
				for (int k = 0; k < m; k++){
					int c1 = strings[j][k] - strings[i][k];
					int c2 = strings[i][k] - strings[j][k];
					if (c1 < 0) c1 = 1399;
					if (c2 < 0) c2 = 1939;
					if (c1 < c2) tans += c1;
					else tans += c2;
					//printf("yo wtf %d %d\n", c1, c2);
					
				}
				if (tans <= ans) ans = tans;
			}
		}
		printf("%d\n", ans);
	}
}
