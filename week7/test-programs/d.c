#include<stdlib.h>
#include<stdio.h>

int g[210][210];
int s[210][210];

int main(){
	int t;
	scanf("%d\n", &t);
	while(t--){
		int n, m;
		scanf("%d %d\n", &n, &m);
		for (int i = 0; i < n; i++){
			for (int j = 0; j < m; j++){
				if (j == m-1) scanf("%d\n", &g[i][j]);
				else scanf("%d ", &g[i][j]);
			}
		}
		int ans = 0;
		for (int i = 0; i < n; i++){
			for (int j = 0; j < m; j++){
				int ci = i, cj = j;
				int s = g[i][j];
				while (--ci >= 0 && --cj >= 0){
					s += g[ci][cj];
				}
				ci = i;
				cj = j;
				while (++ci < n && ++cj < m){
					s += g[ci][cj];
				}
				ci = i;
				cj = j;
				while (--ci >= 0 && ++cj < m){
					s += g[ci][cj];
				}
				ci = i;
				cj = j;
				while (++ci < n && --cj >=0){
					s += g[ci][cj];
				}
				if (s > ans) ans = s;
			}
		}
		printf("%d\n", ans);	
	}
}
