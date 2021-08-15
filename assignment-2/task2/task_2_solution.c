#include <stdio.h>
#include <omp.h>

int omp_odd_counter(int *a, int n){
  int i;
  int count_odd = 0;
  //#pragma omp parallel for shared(a) private(count_odd)
  #pragma omp parallel for shared(a) reduction(+:count_odd)
  for(i=0; i<n; i++) {
    if( a[i] % 2 == 1 ) {
      //#pragma omp critical
      count_odd++;
    }
  }

  return count_odd;
}

int main ()
{
  omp_set_num_threads(4);
  omp_set_schedule(3, 1);

  int n = 15;
  int intList[15]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
  int odds = omp_odd_counter(intList, n);

  printf("%i ", odds);

  return 0;
}
