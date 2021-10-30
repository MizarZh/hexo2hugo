#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import argparse
import logging
import re
import datetime

loggingLevel = logging.WARNING


def wrapper(args):
    logging.info('Staring...')
    main(args.src, args.dest, '')


def main(src, dest, mode):
    src_path = os.path.expanduser(src)
    dest_path = os.path.expanduser(dest)
    markdown = re.compile('\\.md$')

    files = []
    for file in os.listdir(src_path):
        if(markdown.search(file)):
            files.append(file[0:-3])
    logging.info('Total %d files found', len(files))
    for file in files:
        output(file, src_path, dest_path, mode)


def output(file, src, dest, mode):
    srcDirPath = os.path.join(src, file)
    destDirPath = os.path.join(dest, file)  # src + dir
    srcFilePath = os.path.join(src, file + '.md')
    destFilePath = os.path.join(destDirPath, 'index.md')
    # if output folder exists, delete it
    if(os.path.exists(destDirPath)):
        shutil.rmtree(destDirPath)
        logging.info('Folder %s exists', destDirPath)

    if(os.path.exists(srcDirPath)):
        shutil.copytree(srcDirPath, destDirPath)  # copy asset to new folder
        logging.info('Folder %s copying', destDirPath)
    else:
        os.mkdir(destDirPath)
        logging.info('Folder %s creating', destDirPath)

    # shutil.copy2(srcFilePath, destFilePath)  # simply copy markdown article
    process(destFilePath, srcFilePath, mode)

    shutil.copystat(srcFilePath, destDirPath)
    logging.info('MD file "%s" moved', file + '.md')


def process(destFile, srcFile, mode):
    fr = open(srcFile, 'r', encoding='utf-8')
    fw = open(destFile, 'w+', encoding='utf-8')
    line = fr.readline()
    if line == '---\n':
        
        line = fr.readline()
        fw.write('---\n')
        while(line != '---\n'):
            if re.search(r'mathjax:', line):
                fw.write('math: %s'.format(line[re.search(r'mathjax:', line).span()[-1]:]))
            elif re.search(r'tags:', line):
                lastI = re.search(r'tags:', line).span()[-1]
                fw.write('tags:\n')
                if not re.search(r'\s*\n$', line[lastI:]):  # multiple tags
                    fw.write('- ' + line[lastI:].strip(' '))
            # elif re.search(r'date:', line):
                # fw.write(line[:-1] + '+08:00\n')
            else:
                fw.write(line)
            line = fr.readline()
        fw.write('draft: false\n')
        fw.write('---\n')
    fw.write(''.join(fr.readlines()))
    fr.close()
    fw.close()
    shutil.copystat(srcFile, destFile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src', help='source directory')
    parser.add_argument('-o', '--dest', help='destination directory')
    parser.add_argument('-v', '--verbose',
                        help='verbose mode', action='store_true')
    # parser.add_argument('-b')
    # parser.add_argument('-r', '--remove-date', help='remove time file', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        loggingLevel = logging.DEBUG

    format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=loggingLevel, format=format)
    wrapper(args)

# TODO
# open encoding
# 各种格式
# draft
# 时间复制