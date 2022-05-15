#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 10:00:14 2022

@author: lihongyi


this is used to create set of intervals, inspired by leetcode roblem 2276.
"""


class IntervalBisectNode:
    '''
    close interval from stt to end
    '''
    def __init__(self, stt, end):
        self.stt = stt
        self.end = end
        self._n = None
        self._l = None
        self._h
        self.left = None
        self.right = None
    
    def update_nb_and_len(self):
        '''
        set total number of nodes in the tree rooted here 
        and total covered length of nodes in the tree rooted here
        '''
        self._n = 1
        self._l = self.end - self.stt
        self._h = 1
        for cd in [self.left, self.right]:
            if cd is None:
                continue
            self._n += cd.get_nb_nodes()
            self._l += cd.get_len_covered()
            self._h = max(self._h, cd.get_tree_height()+1)
    
    def get_tree_height(self):
        if self._h is None:
            return 1
        return self._h
    
    def get_nb_nodes(self):
        if self._n is None:
            return 1
        return self._n
    
    def get_len_covered(self):
        if self._l is None:
            return self.end - self.stt
        return self._l
    
    def update_left_node(self, left):
        if left is not None:
            assert left.end <= self.stt
            if left.end == self.stt:
                self.stt = left.stt
                self.left = left.left
            else:
                self.left = left
        else:
            self.left = None
        self.update_nb_and_len()
    
    def update_right_node(self, right):
        if right is not None:
            assert right.stt >= self.end
            if right.stt == self.end:
                self.end = right.end
                self.right = right.right
            else:
                self.right = right
        else:
            self.right = None
        self.update_nb_and_len()


def add_new_interval(node, stt, end):
    if node is None:
        return IntervalBisectNode(stt, end)
    
    if stt >= node.stt and end <= node.end:
        return node
    
    if stt > node.end:
        new_right = add_new_interval(node.right, stt, end)
        node.update_right_node(new_right)
        return rotate_tree_single_level(node)
    if end < node.stt:
        new_left = add_new_interval(node.left, stt, end)
        node.update_left_node(new_left)
        return rotate_tree_single_level(node)
    
    if end > node.end:
        new_end, new_right = get_intervers_beyond(node.right, end, True)
        node.end = new_end
        node.update_right_node(new_right)
    if stt < node.stt:
        new_stt, new_left = get_intervers_beyond(node.left, stt, False)
        node.stt = new_stt
        node.update_left_node(new_left)
    # in this case, the tree is not garanteed to be balanced at all levels, 
    # but it won't be worse than adding another leaf node, 
    # in terms of increasing hight
    return rotate_tree_single_level(node)


def rotate_tree_single_level(node):
    if node is None:
        return None
    left_h = 0 if node.left is None else node.left.get_tree_height()
    right_h = 0 if node.right is None else node.right.get_tree_height()
    if right_h > left_h + 1:
        new_root = node.right
        old_root = node
        old_root.update_right_node(new_root.left)
        new_root.update_left_node(old_root)
        return new_root
    if left_h > right_h + 1:
        new_root = node.left
        old_root = node
        old_root.update_left_node(new_root.right)
        new_root.update_right_node(old_root)
        return new_root    
    return node


def get_intervers_beyond(node, limit, right: bool):
    if node is None:
        return limit, None
    
    if right:
        if limit < node.stt:
            new_limit, new_left = get_intervers_beyond(node.left, limit, right)
            node.update_left_node(new_left)
            return new_limit, rotate_tree_single_level(node)
        elif limit <= node.end:
            return node.end, rotate_tree_single_level(node.right)
        else:
            return get_intervers_beyond(node.right, limit, right)
    else:
        if limit > node.end:
            new_limit, new_right = get_intervers_beyond(node.right, limit, right)
            node.update_right_node(new_right)
            return new_limit, rotate_tree_single_level(node)
        elif limit >= node.stt:
            return node.stt, rotate_tree_single_level(node.left)
        else:
            return get_intervers_beyond(node.left, limit, right)


def count_int_covered(node):
    '''all end points have to be integer'''
    if node is None:
        return 0
    return node.get_len_covered() + node.get_nb_nodes()


def print_tree(node):
    if node is None:
        return
    print_tree(node.left)
    print(node.stt, node.end)
    print_tree(node.right)



if __name__ == 'main':
    my_tree = IntervalBisectNode(834,984)
    my_tree = add_new_interval(my_tree, 28,487)
    my_tree = add_new_interval(my_tree, 650,772) 
    my_tree = add_new_interval(my_tree, 706,820)
    my_tree = add_new_interval(my_tree, 824,952) 
    my_tree = add_new_interval(my_tree, 689,990) 
    print_tree(my_tree)




