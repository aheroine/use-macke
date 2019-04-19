#include <assert.h>

void bottom(int i) {
 int re= 42/i;
}

void left(int i) {
  bottom(i);
}

void right(int i) {
  bottom(i);
}

void top(int i) {
  if (i % 2 == 0) {
    left(i);
  } else {
    right(i);
  }
}
void main(int i) {
  if (i % 3 == 0) {
    left(i);
  } else {
    top(i);
  }
}
