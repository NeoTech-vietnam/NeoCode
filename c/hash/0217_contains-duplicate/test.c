// Local tests for 217. Contains Duplicate (not submitted to LeetCode).
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lc.h"
#include "solution.c"

int main(void) {
    int has_duplicate[] = {1, 2, 3, 1};
    int all_distinct[] = {1, 2, 3, 4};
    int mixed[] = {1, 1, 1, 3, 3, 4, 3, 2, 4, 2};
    int single[] = {7};
    int distinct_negative[] = {-1, 0, 5, 100};

    LC_CHECK(containsDuplicate(has_duplicate, 4) == true);
    LC_CHECK(containsDuplicate(all_distinct, 4) == false);
    LC_CHECK(containsDuplicate(mixed, 10) == true);
    LC_CHECK(containsDuplicate(single, 1) == false);
    LC_CHECK(containsDuplicate(distinct_negative, 5) == false);
    return lc_finish();
}
