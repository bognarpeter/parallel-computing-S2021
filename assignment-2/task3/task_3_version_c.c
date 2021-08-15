#include <stdio.h>
#include <omp.h>

int omp_tasks(int v)
{
  printf("omp_tasks is called\n");
  int a, b;
  if( v <= 2 ) {
    return 1;
  } else {
    #pragma omp task shared(a,b)
    a = omp_tasks(v-1);
    #pragma omp task shared(a,b)
    b = omp_tasks(v-2);
    #pragma omp taskwait
    return a + b;
  }
}

void main() {
  int res;
  omp_set_num_threads(4);

  #pragma omp master
  res = omp_tasks(5);

  printf("res=%d\n", res);
}

