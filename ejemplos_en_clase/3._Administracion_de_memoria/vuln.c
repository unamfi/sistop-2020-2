#include <stdio.h>
#include <unistd.h>

int main(int argc, char **argv) {
  char buffer[12];

  if(argc < 2)
    exit(-1);

  strcpy(buffer, argv[1]);
  printf("You wrote %s\n", buffer);
  return 0;
}
