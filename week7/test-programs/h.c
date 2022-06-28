#include<stdlib.h>
#include<stdio.h>

int id = 0;
int f(int a, int b) {return a+b;}

int t[2*200010];

int NN = 200010;

void modify(int p, int value){
	p += NN;
	t[p] += value;
	for (; p/=2; ) t[p] = f(t[2*p], t[2*p+1]);	
}

int query(int l, int r){
	int resl = 0, resr = 0;
	l += NN;
	r += NN;
	for (; l < r; ){
		if (l&1) resl = f(resl, t[l++]);
		if (r&1) resr = f(t[--r], resr);	
		l/=2;
		r/=2;
	}
	return f(resl, resr);
}


int n;
int a[200010];

int compare(const void *a, const void *b){
	const int *ap = a;
	const int *bp = b;
	return *bp - *ap;
}

int main(){
	int test; scanf("%d\n", &test);
	while(test--){
	
		scanf("%d\n", &n);
		for (int i = 0; i <= n; i++) modify(i, -query(i,i+1));
		long long int ans = 0;
		for (int i = 0; i < n; i++){
			if (i == n-1) scanf("%d\n", &a[i]);
			else scanf("%d ", &a[i]); 
		}
		
		for (int i = 0; i < n; i++){
			ans += query(a[i], n+1);
			modify(a[i], 1);
		}
		for (int i = 0; i <= n; i++) modify(i, -query(i,i+1));

		printf("%lld\n", ans); 
	}
}
