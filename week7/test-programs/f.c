#include<stdlib.h>
#include<stdio.h>


int cnt[500010];
int actual[500010];

int n, k;

int hasharr[500010];

int size_of_arr = 0;

int query(int i){
	long long int t = i;
	t = t * 1000003;
	t %= 2*n;
	while (actual[t] != -1 && actual[t] != i){
		t++;
		if (t >= 2*n) t=0;
	}

	actual[t] = i;

	 cnt[t]++;

	if (cnt[t] == k){
		hasharr[size_of_arr++] = i;
	}
	return cnt[t];
}

void reset(){
	size_of_arr = 0;
	for (int i = 0; i < 2*n; i++) {cnt[i] = 0; actual[i] = -1;}
}

int compare (const void *a, const void *b){
	const int *ap = a;
	const int *bp = b;
	return *ap - *bp;
}

int main(){
	int t;
	scanf("%d\n", &t);
	while(t--){
		
		scanf("%d %d\n", &n, &k);
		reset();
		for (int i = 0; i < n; i++){
			int val;
			if (i == n-1) scanf("%d\n", &val);
			else scanf("%d ", &val);
			query(val);
		}
		
		qsort(hasharr, size_of_arr, sizeof(int), compare);
		int ans = 1;
		int l = hasharr[0], r = hasharr[0];
		int len = 1;
		int tl = l, tr = r;
		
		for (int i = 1; i < size_of_arr; i++){
			if (hasharr[i] == tr+1) {
				len++;
				tr++;
			}
			else{
				if (len > ans){
					l = tl;
					r = tr;
					ans = len;
				}
				len = 1;
				tl = hasharr[i];
				tr = hasharr[i];
			}
		}
		if (len > ans){
			l = tl;
			r = tr;
			ans = len;
		}
		if (size_of_arr==0) printf("-1\n");
		else printf("%d %d\n", l, r);
	}
}
