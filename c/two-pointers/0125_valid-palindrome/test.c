// Local tests for 125. Valid Palindrome (not submitted to LeetCode).
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
    //   s = "A man, a plan, a canal: Panama" -> true
    char s1[] = "A man, a plan, a canal: Panama";
    LC_CHECK(isPalindrome(s1) == true);

    //   s = "race a car" -> false
    char s2[] = "race a car";
    LC_CHECK(isPalindrome(s2) == false);

    //   s = " " -> true
    char s3[] = " ";
    LC_CHECK(isPalindrome(s3) == true);
    return lc_finish();
}
