#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import argparse, textwrap, re
from os import path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix a few issues (e.g., attached PDFs, Tags) in the bibtex file exported from Mendeley.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        What does this script do?
        -------------------------
        As for Mendeley v1.19.1, the exported bibtex file has a few issues that
        prevent it from being successfully imported to Zotero (v5.0.52). 
        This script aims to modify the bibtex file you export from Mendeley 
        programmatically, so that it can be appropriately handled by Zotero.

        The issues it deals with are the following:

        1. Fix the format for the attached PDF files.
        2. Fix the mixture of keyword and tags: only the tags you manually input
           into Mendeley are used as tags, but not the author provided keywords.
        3. Fix the escape for some special characters, like "_" or "á".

        Examples
        --------
        python fix_mendeley_bibtex.py -i path/to/exported.bib
        '''))
    parser.add_argument('-i', '--input', required=True, help='')
    args = parser.parse_args()

    word_map = {
        '\{\\\_\}': '_',
        "\{\\\\\'\{a\}\}": 'á',
        "\{\\\\'\{e\}\}": 'é',
        "\{\\\\'\{i\}\}": 'í',
        "\{\\\\'\{o\}\}": 'ó',
        "\{\\\\'\{u\}\}": 'ú',
    }
    output = args.input[:-4] + '_fixed.bib'
    with open(output, 'w') as fo:
        with open(args.input) as fi:
            for line in fi:
                if line[:4] == 'file':
                    parts = line.split(':')
                    fname = parts[1]
                    for k, v in word_map.items():
                        fname = re.sub(k, v, fname)
                    fixed = ':'.join((parts[0]+path.basename(fname), fname, parts[2]))
                elif line[:8] == 'keywords':
                    continue
                elif line[:13] == 'mendeley-tags':
                    parts = line.split(' = ')
                    fixed = 'keywords = ' + parts[1]
                else:
                    fixed = line
                fo.write(fixed)