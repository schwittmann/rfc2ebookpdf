#!/usr/bin/python3

import glob, os, sys
import xml.etree.ElementTree as ET
from multiprocessing import Pool

CREATOR="rfc2ebookpdf (https://github.com/schwittmann/rfc2ebookpdf)"

def pad_rfc_name(name):
    return name[0:3] + "0" * (7-len(name)) + name[3:]

def bulk_convert(rfcall_folder, results_folder, ttf_file, side_margin, top_margin, bookmarks):
    rfc_wildcard=os.path.join(rfcall_folder, "rfc*.txt")
    try:
        os.mkdir(results_folder)
    except:
        pass
    print("Loading RFC meta data...")
    rfc_file_list=glob.glob(rfc_wildcard)
    tree = ET.parse('rfc-index.xml')
    root = tree.getroot()
    print("Found ", len(root.findall("{*}rfc-entry")), "rfc entries.")

    with Pool() as pool:
        for rfc in rfc_file_list:
            rfc_basename=os.path.basename(rfc)[:-4]
            #rfc1234 .txt
            if len(rfc_basename) > 7 or not rfc_basename[3:].isnumeric():
                print("Skipping", rfc)
                continue
            print("Processing", rfc, "...")

            # pad length: rfc137 -> rfc0137
            rfc_basename = pad_rfc_name(rfc_basename)
            pdf_filename=rfc_basename+".pdf"

            pdf_path=os.path.join(results_folder, pdf_filename)
            if os.path.exists(pdf_path):
                print("Skipping existing file ", pdf_filename)
                continue
            try:
                meta_node=root.find("{*}rfc-entry[{*}doc-id='"+rfc_basename.upper()+"']")
                author = ", ".join(map(lambda x:x.text, meta_node.findall("{*}author/{*}name")))
                title = "["+rfc_basename.upper() + "] " + meta_node.find("{*}title").text
                try:
                    keywords = " ".join(map(lambda x:x.text, meta_node.findall("{*}keywords/{*}kw")))
                except TypeError:
                    keywords = ""
                pool.apply_async(PDF_RFC, (rfc, pdf_path, ttf_file, side_margins, top_margin, bookmarks), dict(author=author, title=title, keywords = keywords, creator=CREATOR))
            except Exception as e:
                print ("There was a error with "+rfc+" and the PDF couldn't be generated:", e)


HELP="""bulk_convert.py <rfcs directory> <directory for PDFs> <TTF filename> <side margins> <top_bottom_margin> <generate_bookmarks (use True or False)>.
    
    Example:
        ./bulk_convert RFC-all PDF-Liberation-Mono LiberationMono-Bold.ttf 15 25
        
        The script will take all RFCS in RFC-all and put PDFs in PDF-Liberation-Mono
        where the font used will be LiberationMono-Bold with a lateral margin 
        of 15 and a top and bottom margin of 25. The script will try to generate PDFs
        with bookmarks. For better results is strongly 
        adviced to use a monospaced font."""

if __name__=="__main__" and __package__ is None:
    try:
        from os import sys, path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from rfc2pdf.rfc2pdf import PDF_RFC
        rfc_all_folder = sys.argv[1]
        results_folder = sys.argv[2]
        ttf_file       = sys.argv[3]
        side_margins   = sys.argv[4]
        top_margin     = sys.argv[5]
        bookmarks      = sys.argv[6]
        bulk_convert(rfc_all_folder, results_folder, ttf_file,
        side_margins, top_margin, bookmarks)
    except IndexError:
        print(HELP)
