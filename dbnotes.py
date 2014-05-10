#!/usr/bin/env python
# Douban Notes Grab
# updated May 6 2014

# First parameter is the username, second parameter is the output file path

# Prints all notes into one single file with an output format of:
        # Title
        # Time
        # Content

        # Title
        # Time
        # Content
 
# Note: title is not escaped.

import sys, urllib, re, HTMLParser, time, os
 
def save(url, title, time):
    # the HTML note page
    f = urllib.urlopen(url)
    
    #marks the start of the note
    startstr = '<div class="note" id="link-report">'
    #marks the end of the note
    endstr = '</div>'
    content = ""
    # Flag, if we are saving the content
    saving = False
    for line in f:
        if saving:
            if endstr in line:
                saving = False
                w.write("\nTitle: "+ title + "\nTime: " + time + "\nContent: " + content + "\n")
                print "Finished: " + title
                return          
            else:
                content += line
        else:
            start = line.find(startstr)
            if start != -1:
                content += line[start + len(startstr):]
                saving = True
    
    
def fetch(url):
    print "Start fetching notes from: " + url
    h = HTMLParser.HTMLParser()# for unescaping
    f = urllib.urlopen(url)
    title = None
    time = None
    note_url = None
    for line in f:
        # fetch the title and note url
        m = re.match('.*<a title="([^"]*)" href="([^"]*)">(.*)</a>', line)
        if m:
            # UnicodeDecodeError 
            #title = h.unescape(m.group(3).decode("utf-8"))
            title = m.group(3)
            note_url = m.group(2)
            continue
        # fetch the time
        m = re.match('.*<span class="pl">([^<]*)</span>', line)
        if m:
            time = m.group(1)
            # save this note to the file
            save(note_url, title, time)
            continue
        # fetch the next page of a list of notes
        m = re.match('.*<link rel="next" href="([^"]*)"/>', line)
        if m:  
            return m.group(1)
        # don't fetch things on the side column
        m = re.match('.*<div class="aside">.*', line)
        if m:  
            return
    return None

# Prompt
if len(sys.argv) < 2:
    print "usage: %s <douban id> <output filepath>" % sys.argv[0]
    sys.exit(1)
 
userid = sys.argv[1]
fname = sys.argv[2]
w = open(fname, "w")
        
url = "http://www.douban.com/people/%s/notes" % userid
while url != None:
    url = fetch(url)

w.close()