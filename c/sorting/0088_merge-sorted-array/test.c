// Local tests for 88. Merge Sorted Array (not submitted to LeetCode).
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lc.h"
#include "solution.c"

int main(void) {
    // Examples from LeetCode (input -> expected output):
    //   nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3 -> [1,2,2,3,5,6]
    //   nums1 = [1], m = 1, nums2 = [], n = 0 -> [1]
    //   nums1 = [0], m = 0, nums2 = [1], n = 1 -> [1]
    int nums1_example1[] = {1, 2, 3, 0, 0, 0};
    int nums2_example1[] = {2, 5, 6};
    int expected_example1[] = {1, 2, 2, 3, 5, 6};
    merge(nums1_example1, 6, 3, nums2_example1, 3, 3);
    LC_CHECK(lc_int_array_equals(nums1_example1, 6, expected_example1, 6));

    int nums1_example2[] = {1};
    int nums2_example2[] = {0};
    int expected_example2[] = {1};
    merge(nums1_example2, 1, 1, nums2_example2, 0, 0);
    LC_CHECK(lc_int_array_equals(nums1_example2, 1, expected_example2, 1));

    int nums1_example3[] = {0};
    int nums2_example3[] = {1};
    int expected_example3[] = {1};
    merge(nums1_example3, 1, 0, nums2_example3, 1, 1);
    LC_CHECK(lc_int_array_equals(nums1_example3, 1, expected_example3, 1));
    return lc_finish();
}
