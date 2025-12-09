#include "progress.h"

void progressBar(int percent) {
  const int barWidth = 50;
  int pos = (percent * barWidth) / 100;

  printf("\r[");
  for (int i = 0; i < barWidth; i++) {
    if (i < pos) printf("▒");
    else if (i == pos) printf("▓");
    else printf("░");
  }
  printf("] %d%%", percent);
  fflush(stdout);
}