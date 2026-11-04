#define _GNU_SOURCE
#include <dlfcn.h>
#include <time.h>
typedef struct GLFWwindow GLFWwindow;
static struct timespec last;
void glfwSwapBuffers(GLFWwindow* w){
  static void (*real)(GLFWwindow*) = 0;
  if(!real) real = dlsym(RTLD_NEXT, "glfwSwapBuffers");
  real(w);
  struct timespec now; clock_gettime(CLOCK_MONOTONIC,&now);
  long el = (now.tv_sec-last.tv_sec)*1000000000L + (now.tv_nsec-last.tv_nsec);
  long want = 16666667L;
  if(last.tv_sec && el < want){ struct timespec s={0,want-el}; nanosleep(&s,0); }
  clock_gettime(CLOCK_MONOTONIC,&last);
}
