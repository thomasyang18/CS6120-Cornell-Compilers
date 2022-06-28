#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
	int n;
	scanf("%d\n", &n);
	for (int i = 0; i < n; i++){
		int s = 0;
		char str[7];
		scanf("%s\n", str);
		//printf("%s\n", str);
		for (int j = 0; j < 3; j++) s += str[j];
		for (int j = 3; j < 6; j++) s -= str[j];
		if (!s) printf("YES\n"); else printf("NO\n");
		
	}
}
