# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:33:58 2020

@author: bransonngai
"""

#import PyPDF2
#import pdfplumber


from argparse import ArgumentParser
import pickle
import pprint
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdftypes import resolve1, PDFObjRef

def load_form(filename):
    """Load pdf form contents into a nested list of name/value tuples"""
    with open(filename, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()
        return [load_fields(resolve1(f)) for f in
                   resolve1(doc.catalog['AcroForm'])['Fields']]

def load_fields(field):
    """Recursively load form fields"""
    form = field.get('Kids', None)
    if form:
        return [load_fields(resolve1(f)) for f in form]
    else:
        # Some field types, like signatures, need extra resolving
        return (field.get('T').decode('utf-16'), resolve1(field.get('V')))

def parse_cli():
    """Load command line arguments"""
    parser = ArgumentParser(description='Dump the form contents of a PDF.')
    parser.add_argument('file', metavar='pdf_form',
                    help='PDF Form to dump the contents of')
    parser.add_argument('-o', '--out', help='Write output to file',
                      default=None, metavar='FILE')
    parser.add_argument('-p', '--pickle', action='store_true', default=False,
                      help='Format output for python consumption')
    return parser.parse_args()

def main():
    args = parse_cli()
    form = load_form(args.file)
    if args.out:
        with open(args.out, 'w') as outfile:
            if args.pickle:
                pickle.dump(form, outfile)
            else:
                pp = pprint.PrettyPrinter(indent=2)
                file.write(pp.pformat(form))
    else:
        if args.pickle:
            print(pickle.dumps(form))
        else:
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(form)

if __name__ == '__main__':
    main()