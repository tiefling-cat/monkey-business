#!/usr/bin/env python3

import os
import sys
import lzma
from argparse import ArgumentParser

AFORM, ALEMMA, ATAGS, AORD, AHEAD, AFUNC = range(6)
TLEMMA, TFUNC, TORD, THEAD, TYPE, TTAGS = range(6)
LAYERS = {'a': [AFORM, ALEMMA, ATAGS, AORD, AHEAD, AFUNC],
          't': [TLEMMA, TFUNC, TORD, THEAD, TYPE, TTAGS]}
HEAD = {'a': AHEAD, 't': THEAD}
ORD = {'a': AORD, 't': TORD}

def str_to_tree(line, layer, whole=None):
    '''
    Convert str representation of a single tree
    from input files into a list representing
    the tree.
    '''
    feats = LAYERS[layer]
    head_pos = HEAD[layer]
    children_pos = len(feats)

    # parse tree
    root = ['ROOT', 'ROOT'] + [''] * (len(feats) - 2) + [[]]
    tree = [root]
    for token_str in line.split(' '):
        token_feats = token_str.split('|')[:children_pos] + [[]]
        tree.append(token_feats)

    # add children
    for i in range(1, len(tree)):
        head = int(tree[i][head_pos])
        tree[head][children_pos].append(i)

    return tree

def tree_to_linear(tree, pos):
    output = []
    for token in tree:
        output.append(token[pos])
    return ' '.join(output)

def tree_to_dfs(tree, layer, pos):
    head_pos = HEAD[layer]
    ord_pos = ORD[layer]

    # root -> stack
    stack = [tree[0]]
    traversal = []
    while stack != []:
        top = stack.pop()
        traversal.append(top[pos])
        # children -> stack
        for child_ord in top[-1][::-1]:
            stack.append(tree[child_ord])

    return ' '.join(traversal)

def prepare_data(args, dataset):
    '''
    Go through all xz files in input folder,
    extract the data and output it
    to the respective output files.
    '''
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)

    file_list = sorted(filter(lambda x: x.endswith('.xz') and dataset in x,
                              os.listdir(args.in_folder)))

    for file_name in file_list:
        with lzma.open(file_name, 'rt', encoding='utf-8') as in_file:
            for line in in_file:
                split = line.strip().split('\t')
                source_a, source_t = split[2:4]
                target_a, target_t = split[6:8]

                source_a_tree = str_to_tree(source_a, 'a')
                target_a_tree = str_to_tree(target_a, 'a')


if __name__ == '__main__':
    parser = ArgumentParser(description='Prepare CZENG data.')
    parser.add_argument('-f', '--in-folder', metavar='IN_FOLDER', type=str,
                        action='store', dest='in_folder',
                        help='folder with raw data')
    parser.add_argument('-o', '--out-folder', metavar='OUT_FOLDER', type=str,
                        action='store', dest='out_folder',
                        help='folder for the output')

    args = parser.parse_args()

    prepare_data(args, 'train')
