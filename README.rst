.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/herrlich10/men2zot/blob/master/LICENSE.txt

Overview
========
This package contains a few small Python scripts that help you deal with 
the problems you may encounter when you move from Mendeley to Zotero:

1. The associations with the PDF files are not preserved.
2. Both author-provided keywords and user-specified tags are imported as tags.
3. The dates you added the entries are not preserved.

This package is not a comprehensive tool that does all the jobs in one shot. 
But it indeed helped me solve all the above problems. At least, it can be used 
as the starting point for your own solution, as the Python codes are short and 
easy to read.

This package has no unusual dependencies beyond numpy and pandas. So it should 
work out of the box if you have Anaconda installed. 

Bugs can be reported to https://github.com/herrlich10/men2zot. 
The code can also be found there.

Basic workflow
==============
1. Export your Mendeley library as a bibtex file, e.g., ``test.bib``.

    **NOTE:** You may want to test on a small export with only a few items first. 
 
    **NOTE:** Some of the scripts work directly on the sqlite databases of both programs.
    Always **backup** your sqlite files before letting this script change them.

2. Fix the bibtex file using ``fix_mendeley_bibtex.py``::

    python fix_mendeley_bibtex.py -i test.bib

3. Import the resulting ``test_fixed.bib`` into Zotero.

4. Transfer added date using ``mendeley2zotero.py``::

    python mendeley2zotero.py -m path/to/mendeley.sqlite -z path/to/zotero.sqlite

5. Check your Zotero library to see whether there are remaining problems.

Related works
=============
Mendeley is a good reference manager in many ways. However, its limitations become
increasingly unaffordable in recent releases. Among the top of the list is that 
it has the potential to lock its users in. It is not easy to get all your personal 
data out of Mendeley when you decide to leave. There are a few other projects out 
there already to mitigate these difficulties:

- Mendeley2Zotero_: written in Python, transfer dates, folders
- Adios_Mendeley_: written in R, transfer notes, dates, folders/collections, and PDF annotations

.. _Mendeley2Zotero: https://github.com/flinz/mendeley2zotero
.. _Adios_Mendeley: https://github.com/rdiaz02/Adios_Mendeley

See also discussions in the Zotero forum:

- https://forums.zotero.org/discussion/63737/moving-library-from-mendeley-to-zotero
- https://forums.zotero.org/discussion/30349/import-pdfs-from-mendeley-to-zotero


I didn't create multiple folders (only use tags), nor create notes/highlights from
within Mendeley (only use PDF reader). But I did have problems with PDF (attachment) 
associations and tags that the above authors did not mention. And unfortunately 
Mendeley2Zotero didn't work for me. So I created these simple Python scripts. 
Hope they helps. And I'm very happy to work with a fully open reference manager now~
