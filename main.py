#!/usr/bin/env python3


import ebooklib
import sys
import os
from ebooklib import epub
from bs4 import BeautifulSoup
from summarize import summarize


blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script',   ]
# there may be more elements you don't want, such as "style", etc

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output


def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

def empty_sandbox():
    print("Emptying sandbox directory...")
    for f in os.listdir("Sandbox/"):
        os.remove("Sandbox/" + str(f))


def convert_book(filepath):
    filename, file_extension = os.path.splitext(filepath)
    if file_extension == ".txt":
        # open both files
        firstfile =  open(filepath,'r')
        bookfile = open('./Sandbox/book.txt','a')
        for line in firstfile:
            secondfile.write(line)
        close(filepath)
        close(bookfile)
    elif file_extension == ".epub":
        book = epub2text(filepath)
        f = open("Sandbox/book.txt", 'a')
        for line in book:
            f.write(line)
        f.close
    else:
        print(file_extension)
        print("File format not supported!")
    name = filename.split("/")
    return name[len(name) - 1]

def split_chapterwise():
    f = open("Sandbox/book.txt", "r")
    entire_book = f.read()
    text_splitter = "Chapter"
    if "Chapter" in entire_book:
        text_splitter = "Chapter"
    elif "CHAPTER" in entire_book:
        text_splitter = "CHAPTER"
    chapters = entire_book.count(text_splitter)
    print("Your book has " + str(chapters) + " chapters")
    chaps = entire_book.split(text_splitter)
    for i in range(len(chaps)):
        chap = open("Sandbox/Chapter" + str(i) + ".txt", "a")
        chap.write(chaps[i])
        chap.close
    print("Finished splitting your book into chapters")
    return chapters


def summarize_book(bookname, chapters):
    os.mkdir("Summaries/" + bookname)
    for i in range(chapters):
        print("Summarizing Chapter " + str(i+1))
        chapter = "Chapter" + str(i+1) + ".txt"
        summarize_chapter("Sandbox/" + chapter, "Summaries/" + bookname  + "/"+ chapter)


def summarize_chapter(inputpath, outputpath):
    f = open(inputpath)
    output = open(outputpath, "a")
    text = f.read()
    summary = text
    summary = summarize(text)
    output.write(summary)
    f.close
    output.close

    output.write(summary)
    print("Successfully done summarizing")

def main():
    if len(sys.argv) <= 1:
        print("Please provide a file to summarize")
        return
    if not os.path.exists("Summaries"):
        os.makedirs("Summaries")
    if not os.path.exists("Sandbox"):
        os.makedirs("Sandbox")

    for i in range(1,len(sys.argv)):
        empty_sandbox()
        bookname = convert_book(sys.argv[i])
        print("Beginning to summarize " + bookname)
        chapters = split_chapterwise()
        summarize_book(bookname, chapters)

main()
