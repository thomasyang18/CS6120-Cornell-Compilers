#include <stdlib.h>
#include <stdio.h>


int a[200010];
int p[200010];
int compare(const void *a, const void *b){
	const int *ap = a;
	const int *bp = b;
	return *bp - *ap;
}

int main(){
	int t;
	scanf("%d\n", &t);
	while(t--){
		int n, q;
		scanf("%d %d\n", &n, &q);
		for (int i = 0; i < n; i++){
			if (i == n-1) scanf("%d\n", &a[i]);
			else scanf("%d ", &a[i]);
		}
		qsort(a, n, sizeof(int), compare);
		for (int i = 0; i < n; i++){
			p[i] = a[i];
			if (i > 0) p[i] += p[i-1];
		}
		while(q--){int tar;
		scanf("%d\n", &tar);
		int l = -1, r = n;
		while (l+1<r){
			int m = (l+r)/2;
			if (p[m] >= tar) r = m;
			else l = m;
		}
		if (r == n) printf("-1\n");
		else printf("%d\n", r+1);
		}
	}
}
