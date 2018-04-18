#!/usr/bin/env python3

import os
import sys
import lzma
from argparse import ArgumentParser
from collections import deque

AFORM, ALEMMA, ATAGS, AORD, AHEAD, AFUNC = range(6)
TLEMMA, TFUNC, TORD, THEAD, TYPE, TTAGS = range(6)
LAYERS = {'a': [AFORM, ALEMMA, ATAGS, AORD, AHEAD, AFUNC],
          't': [TLEMMA, TFUNC, TORD, THEAD, TYPE, TTAGS]}
HEAD = {'a': AHEAD, 't': THEAD}
ORD = {'a': AORD, 't': TORD}

core_args = ('ACT', 'PAT', 'EFF', 'ADDR', 'ORIG')

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
        if token_str != '':
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
    return ' '.join(output[1:])

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

    return ' '.join(traversal[1:])

def tree_to_bfs(tree, layer, pos):
    head_pos = HEAD[layer]
    ord_pos = ORD[layer]

    # root -> queue
    queue = deque([tree[0]])
    traversal = []
    while len(queue) != 0:
        top = queue.popleft()
        traversal.append(top[pos])
        # children -> queue
        for child_ord in top[-1]:
            queue.append(tree[child_ord])

    return ' '.join(traversal[1:])

def t_tree_to_frames(tree):
    frames = []
    for token in tree:
        if token[TFUNC] == 'PRED':
            frame = token[TLEMMA] + ' | ' +\
                    ' '.join([tree[child][TLEMMA]
                              for child in token[-1]
                              if tree[child][TFUNC] in core_args])
            frames.append(frame)
    return ' ; '.join(frames)

def prepare_data(args, in_dataset, out_dataset, offset=0, max_sentence_count=1000000):
    '''
    Go through all xz files in input folder,
    extract the data and output it
    to the respective output files.
    '''
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)

    file_list = sorted(filter(lambda x: x.endswith(dataset + '.xz') and dataset in x,
                              os.listdir(args.in_folder)))

    source_lin_path = os.path.join(args.out_folder, dataset + '.lin.cz')
    source_dfs_path = os.path.join(args.out_folder, dataset + '.dfs.cz')
    source_bfs_path = os.path.join(args.out_folder, dataset + '.bfs.cz')
    source_fra_path = os.path.join(args.out_folder, dataset + '.fra.cz')
    target_path = os.path.join(args.out_folder, dataset + '.en')

    seen_sentence_count = 0
    output_sentence_count = 0

    with open(source_lin_path, 'w', encoding='utf-8') as source_lin_file,\
         open(source_dfs_path, 'w', encoding='utf-8') as source_dfs_file,\
         open(source_bfs_path, 'w', encoding='utf-8') as source_bfs_file,\
         open(source_fra_path, 'w', encoding='utf-8') as source_fra_file,\
         open(target_path, 'w', encoding='utf-8') as target_file:

        for file_name in file_list:
            file_path = os.path.join(args.in_folder, file_name)
            with lzma.open(file_path, 'rt', encoding='utf-8') as in_file:
                for line in in_file:
                    split = line.strip().split('\t')
                    source_a, source_t = split[2:4]
                    target_a, target_t = split[6:8]

                    if source_t != '':

                        source_a_tree = str_to_tree(source_a, 'a')
                        target_a_tree = str_to_tree(target_a, 'a')

                        source_t_tree = str_to_tree(source_t, 't')

                        if len(source_t_tree) != 0:
                            if seen_sentence_count >= offset:
                                # there might not be a t-tree on either side
                                print(tree_to_linear(source_a_tree, AFORM),
                                      file=source_lin_file)
                                print(tree_to_linear(target_a_tree, AFORM),
                                      file=target_file)
                                print(tree_to_dfs(source_a_tree, 'a', AFORM),
                                      file=source_dfs_file)
                                print(tree_to_bfs(source_a_tree, 'a', AFORM),
                                      file=source_bfs_file)
                                print(t_tree_to_frames(source_t_tree),
                                      file=source_fra_file)
                                output_sentence_count += 1
                            seen_sentence_count += 1

                    if output_sentence_count >= max_sentence_count:
                        return


if __name__ == '__main__':
    parser = ArgumentParser(description='Prepare CZENG data.')
    parser.add_argument('-f', '--in-folder', metavar='IN_FOLDER', type=str,
                        action='store', dest='in_folder',
                        default = '/net/data/czeng17/data.export-format',
                        help='folder with raw data')
    parser.add_argument('-o', '--out-folder', metavar='OUT_FOLDER', type=str,
                        action='store', dest='out_folder',
                        default='/net/work/people/mediankin/snmt/data/czeng',
                        help='folder for the output')

    args = parser.parse_args()

    prepare_data(args, in_dataset='train', out_dataset='train', max_sentence_count=1000000)
    prepare_data(args, in_dataset='dtest', out_dataset='dev', max_sentence_count=2000)
    prepare_data(args, in_dataset='dtest', out_dataset='test', offset=2000, max_sentence_count=5000)
