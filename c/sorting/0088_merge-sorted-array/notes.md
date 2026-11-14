# 88. Merge Sorted Array

- **Problem:** https://leetcode.com/problems/merge-sorted-array/
- **Pattern:**
- **Status:** AC with help / AC on my own / Re-solved independently

## Problem

Merge the first `m` elements of sorted `nums1` with the `n` elements of sorted `nums2`. Store the merged array in `nums1`, which has room for all `m + n` elements. The remaining `n` slots of `nums1` are placeholders and should be ignored.

- **Constraints:** `nums1.length == m + n`; `nums2.length == n`; `0 <= m, n <= 200`; `1 <= m + n <= 200`; `-10^9 <= nums1[i], nums2[j] <= 10^9`; both arrays are sorted in non-decreasing order.

## Examples

- Input: `nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3` → Output: `[1,2,2,3,5,6]`
- Input: `nums1 = [1], m = 1, nums2 = [], n = 0` → Output: `[1]`
- Input: `nums1 = [0], m = 0, nums2 = [1], n = 1` → Output: `[1]`

## Edge cases to consider

- What should happen when `m` or `n` is zero?
- What if the arrays contain equal values?
- What if values include `-10^9` or `10^9`?
- What inputs use the maximum allowed combined length?

## Why it is correct

## Complexity

- Time:
- Space:

## Edge cases and mistakes

## Re-solves

| Date | Without looking at the answer? | Time | Notes |
| --- | --- | --- | --- |
