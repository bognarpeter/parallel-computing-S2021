#include <stdio.h>
#include <omp.h>

int main ()
{
  int n = 15;
  int thread_num = 4;
  omp_set_num_threads(thread_num);
  omp_set_schedule(3, 2);
  int a[15] = {};
  int t[4] = {};

  #pragma omp parallel for schedule(runtime)
  for (int i = 0; i < n; i++){
    a[i] = omp_get_thread_num ();
    t[omp_get_thread_num ()]++;
    }

  printf("Contents of a: \na[");
  for (int i = 0; i < n; i++)
  {
    printf("%i & ", a[i]);
  }
  printf("]");

  printf("Contents of t: \nt[");
  for (int i = 0; i < thread_num; i++)
  {
    printf("%i & ", t[i]);
  }
  printf("]");
  return 0;
}
