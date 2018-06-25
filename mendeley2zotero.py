#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import sys, argparse, textwrap, shutil
from os import path
import sqlite3
import numpy as np
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transfer "Added Date" from Mendeley to Zotero by manipulating the sqlite database directly.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        Examples
        --------
        python mendeley2zotero.py -m "/Users/your_name/Library/Application Support/Mendeley Desktop/your_account@www.mendeley.com.sqlite" -z /Users/your_name/Zotero/zotero.sqlite
        '''))
    parser.add_argument('-m', '--mendeley', required=True, help='path to Mendeley sqlite file')
    parser.add_argument('-z', '--zotero', required=True, help='path to Zotero sqlite file')
    args = parser.parse_args()

    # Backup zotero database
    bak_file = args.zotero + '.bak'
    if not path.exists(bak_file):
        shutil.copy(args.zotero, bak_file)
    else:
        print('>> Backup file "{0}" already exists. You need to manually restore it first.'.format(bak_file))
        print('>> The program will quit for now, without making any changes.')
        sys.exit(1)
    # Open database
    m_conn = sqlite3.connect(args.mendeley)
    m_cur = m_conn.cursor()
    z_conn = sqlite3.connect(args.zotero)
    z_cur = z_conn.cursor()
    # Construct DataFrames with necessary information
    mdf = pd.read_sql_query("SELECT title, added from Documents", m_conn)
    mdf.added = pd.to_datetime(mdf.added, unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    zdf = pd.read_sql_query('''
        SELECT items.itemID, itemDataValues.valueID, value, dateAdded 
        FROM (items INNER JOIN itemData ON items.itemID=itemData.itemID)
        INNER JOIN itemDataValues ON itemData.valueID=itemDataValues.valueID 
        WHERE fieldID=110 and itemTypeID!=14
        ''', z_conn) # fieldID=110 is "title", and itemTypeID=14 is "attachment"
    # Substitute dateAdded in zotero database
    n = 0
    for k in range(len(zdf)):
        title_match = np.nonzero(mdf.title==zdf.value[k])[0]
        if title_match.size > 0:
            m_date = mdf.added[title_match[0]]
            res = z_cur.execute(f'UPDATE items SET dateAdded="{m_date}" WHERE itemID="{zdf.itemID[k]}";')
            if res.rowcount > 0:
                n += 1
    z_conn.commit() # Write sqlite file
    print('>> {0}({1}) items updated.'.format(n, len(zdf)))
    # Close database
    m_conn.close()
    z_conn.close()
