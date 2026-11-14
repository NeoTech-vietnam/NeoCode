/*
 * lc.h - helpers for local tests (test.c / test.cpp) only.
 *
 * Never paste this into LeetCode: LeetCode already defines ListNode and TreeNode.
 * Works in C11 and C++17/20. Every function is static inline so unused helpers do
 * not trigger warnings under -Wall -Wextra -Werror.
 */
#ifndef LC_H
#define LC_H

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef __cplusplus
#include <vector>
#else
#include <stdbool.h>
#endif

/* Marks a missing node in lc_tree_from_level(), like "null" in LeetCode's [1,null,2]. */
#define LC_NULL INT_MIN

/* ---- Data structures, exactly as LeetCode defines them ---- */

#ifdef __cplusplus
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};
#else
struct ListNode {
    int val;
    struct ListNode *next;
};

struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};
#endif

/* ---- Checks ---- */

static inline int *lc_counters_(void) {
    static int counters[2]; /* [0] = checks, [1] = failures */
    return counters;
}

static inline void lc_check_(int ok, const char *expr, const char *file, int line) {
    int *counters = lc_counters_();
    counters[0]++;
    if (!ok) {
        counters[1]++;
        printf("FAIL %s:%d: LC_CHECK(%s)\n", file, line, expr);
        fflush(stdout);
    }
}

/* LC_CHECK(expr): count one check; print the location and the expression if it is false. */
#define LC_CHECK(...) lc_check_((__VA_ARGS__) ? 1 : 0, #__VA_ARGS__, __FILE__, __LINE__)

/* Print the summary line read by tools/build_test.py; return its value from main(). */
static inline int lc_finish(void) {
    int *counters = lc_counters_();
    printf("LC-RESULT checks=%d failed=%d\n", counters[0], counters[1]);
    fflush(stdout);
    return counters[1] != 0 ? 1 : 0;
}

/* ---- Allocation (malloc/free in C, new/delete in C++, as LeetCode does) ---- */

static inline void *lc_alloc_(size_t size) {
    void *p = malloc(size);
    if (p == NULL) {
        fprintf(stderr, "lc.h: out of memory\n");
        exit(2);
    }
    return p;
}

static inline struct ListNode *lc_list_node_(int val) {
#ifdef __cplusplus
    return new ListNode(val);
#else
    struct ListNode *node = (struct ListNode *)lc_alloc_(sizeof *node);
    node->val = val;
    node->next = NULL;
    return node;
#endif
}

static inline void lc_list_node_free_(struct ListNode *node) {
#ifdef __cplusplus
    delete node;
#else
    free(node);
#endif
}

static inline struct TreeNode *lc_tree_node_(int val) {
#ifdef __cplusplus
    return new TreeNode(val);
#else
    struct TreeNode *node = (struct TreeNode *)lc_alloc_(sizeof *node);
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
#endif
}

static inline void lc_tree_node_free_(struct TreeNode *node) {
#ifdef __cplusplus
    delete node;
#else
    free(node);
#endif
}

/* ---- Arrays ---- */

static inline bool lc_int_array_equals(const int *a, int an, const int *b, int bn) {
    if (an != bn) {
        return false;
    }
    for (int i = 0; i < an; i++) {
        if (a[i] != b[i]) {
            return false;
        }
    }
    return true;
}

static inline void lc_print_int_array(const int *a, int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        if (i > 0) {
            printf(",");
        }
        printf("%d", a[i]);
    }
    printf("]\n");
}

/* ---- Linked lists ---- */

/* Build a list from a[0..n-1]; free it with lc_list_free(). */
static inline struct ListNode *lc_list_from_array(const int *a, int n) {
    struct ListNode *head = NULL;
    struct ListNode **tail = &head;
    for (int i = 0; i < n; i++) {
        *tail = lc_list_node_(a[i]);
        tail = &(*tail)->next;
    }
    return head;
}

static inline bool lc_list_equals_array(const struct ListNode *head, const int *a, int n) {
    int i = 0;
    for (; head != NULL; head = head->next, i++) {
        if (i >= n || head->val != a[i]) {
            return false;
        }
    }
    return i == n;
}

static inline void lc_list_free(struct ListNode *head) {
    while (head != NULL) {
        struct ListNode *next = head->next;
        lc_list_node_free_(head);
        head = next;
    }
}

/* ---- Binary trees ---- */

/* Build a tree from LeetCode's level order, e.g. {1, LC_NULL, 2, 3}; free it with lc_tree_free(). */
static inline struct TreeNode *lc_tree_from_level(const int *a, int n) {
    if (n <= 0 || a[0] == LC_NULL) {
        return NULL;
    }
    /* FIFO of nodes still waiting for their children; each node enters it once. */
    struct TreeNode **pending = (struct TreeNode **)lc_alloc_((size_t)n * sizeof *pending);
    int head = 0;
    int tail = 0;
    int i = 1;
    struct TreeNode *root = lc_tree_node_(a[0]);
    pending[tail++] = root;
    while (head < tail && i < n) {
        struct TreeNode *node = pending[head++];
        if (a[i] != LC_NULL) {
            node->left = lc_tree_node_(a[i]);
            pending[tail++] = node->left;
        }
        i++;
        if (i < n && a[i] != LC_NULL) {
            node->right = lc_tree_node_(a[i]);
            pending[tail++] = node->right;
        }
        i++;
    }
    free(pending);
    return root;
}

static inline void lc_tree_free(struct TreeNode *root) {
    if (root == NULL) {
        return;
    }
    lc_tree_free(root->left);
    lc_tree_free(root->right);
    lc_tree_node_free_(root);
}

/* ---- C++ overloads taking std::vector<int> ---- */

#ifdef __cplusplus
static inline bool lc_int_array_equals(const std::vector<int> &a, const std::vector<int> &b) {
    return a == b;
}

static inline void lc_print_int_array(const std::vector<int> &v) {
    lc_print_int_array(v.data(), static_cast<int>(v.size()));
}

static inline ListNode *lc_list_from_array(const std::vector<int> &v) {
    return lc_list_from_array(v.data(), static_cast<int>(v.size()));
}

static inline bool lc_list_equals_array(const ListNode *head, const std::vector<int> &v) {
    return lc_list_equals_array(head, v.data(), static_cast<int>(v.size()));
}

static inline TreeNode *lc_tree_from_level(const std::vector<int> &v) {
    return lc_tree_from_level(v.data(), static_cast<int>(v.size()));
}
#endif

#endif /* LC_H */
