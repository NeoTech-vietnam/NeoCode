// Local tests for 2235. Add Two Integers (not submitted to LeetCode).
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lc.h"
#include "solution.c"

int main(void) {
    LC_CHECK(sum(12, 5) == 17);
    LC_CHECK(sum(-10, 4) == -6);
    LC_CHECK(sum(0, 0) == 0);
    LC_CHECK(sum(-100, -100) == -200);
    LC_CHECK(sum(100, 100) == 200);
    return lc_finish();
}
