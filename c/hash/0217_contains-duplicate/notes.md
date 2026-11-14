# 217. Contains Duplicate

- **Problem:** https://leetcode.com/problems/contains-duplicate/
- **Pattern:** Hash set (or sort then scan)
- **Status:** AC with help / AC on my own / Re-solved independently

## Problem

Given an integer array `nums`, return `true` if any value appears at least twice, and `false` if every element is distinct.

- **Constraints:** `1 <= nums.length <= 10^5`, `-10^9 <= nums[i] <= 10^9`

## Examples

- Input: `nums = [1,2,3,1]` → Output: `true`
- Input: `nums = [1,2,3,4]` → Output: `false`
- Input: `nums = [1,1,1,3,3,4,3,2,4,2]` → Output: `true`

## Hints

- What do you need to remember about the elements you have already seen?
- Sorting puts equal values next to each other; what trade-off does that cost?
- A hash set gives near-constant lookup, but you may need to handle collisions.

## Why it is correct

## Complexity

- Time:
- Space:

## Edge cases and mistakes

- Empty array: the constraints say it cannot happen, but decide what your function should do.
- Single element: no duplicate is possible.
- Duplicates at the two ends of the array.
- All elements distinct.
- Large negative and positive values.

## Re-solves

| Date | Without looking at the answer? | Time | Notes |
| --- | --- | --- | --- |
