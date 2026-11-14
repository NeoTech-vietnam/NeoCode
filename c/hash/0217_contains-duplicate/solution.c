// 217. Contains Duplicate
// https://leetcode.com/problems/contains-duplicate/
// Paste-ready for LeetCode: keep only the LeetCode function here (no main, no tests).

bool containsDuplicate(int* nums, int numsSize) {

    for (int i = 0; i < numsSize; i++)
    {
        for (int j = i; j < numsSize; j++)
        {
            if (nums[j] == nums[i])
            {
                return true;
            }
        }
    }

    return false;
}
