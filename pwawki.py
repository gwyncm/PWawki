#! /usr/local/bin/python3
#
#
#

import os,re,sys,string

H    = 0
PRE  = 0
UL   = 0
OL   = 0
TABL = 0
CGI  = "YES"
EDIT = "1"
PAGE = "NOPAGE"
DATE = "000000"
VALUES = {}
LINK = ""
IMG = ""
LAB = ""

#
# Print page header
#
def beginPage() :
  global PAGE
  print("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
  print("<html xmlns=\"http://www.w3.org/1999/xhtml\">")
  print("<html><head><title>",PAGE,"</title>")
  print("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://gwynux.ca/css/formatter.css\"></head>")
#
# Print page trailer
#
def endPage() :
  global H
  global CGI
  global PAGE
  global DATE
  print("<p><hr>")
  if "YES" == CGI :
    print("<a href=\"wawki.cgi?HomePage\">Home</a>")
    if  EDIT == "1" : print("  <a href=\"wawki.cgi?@{0:s}\">Edit</a>".format(PAGE))
    print("| ",end=' ')
  print("Last Modified: ",DATE)
  print("<hr></body></html>")
#
# Process input line
#
def processLine(line) :
  global H
  global PRE
  global UL
  global OL
  global LINK
  global IMG
  global TABL
  global LAB
  if re.match(" *$",line) : print("<p>")
  for CF in line.split(' ') :
    if PRE == 1 :
      if re.search("@@$",CF) : 
        CF=re.sub("@@$","</pre>",CF) ; PRE = 0
      if re.search("@[!]@",CF) : CF=re.sub("[!]","",CF)	# Fake null	
      print(CF,end=" ") 
      continue
#
    if re.match("@@",CF) : 
      CF=re.sub("@@","<pre>",CF) ; PRE = 1
#
#	Value <<=NAME:VALUE=>> 
#
    if re.match("<<=",CF) : 
      CF=re.sub("<<=","",CF) 
      CF=re.sub("=>>","",CF) 
      CS=re.sub(".*:","",CF)
      CF=re.sub(":.*","",CF)
      VALUES [CF] = CS
      CF = ""
#
#	Field <<:NAME:SIZE:>> 
#
    if re.match("<<:",CF) : 
      CF=re.sub("<<:","",CF) 
      CF=re.sub(":>>","",CF) 
      CS=re.sub(".*:","",CF)
      CF=re.sub(":.*","",CF)
      VA = ""
      if CF in VALUES : VA = VALUES[CF]
      print("<input type=\"text\" name=\"{0:s}\" size=\"{1:s}\" value=\"{2:s}\">".format(CF,CF,VA)) 
      CF = ""
#
#	Button <<$ BUTTON  $>> 
#
    if re.match("<<\$",CF) : 
      CF=re.sub("<<\$","",CF) 
      CF=re.sub("\$>>","",CF) 
      print("<input type=submit value=\"{0:s}\">".format(CF)) 
      CF = ""
#
#	Form << ACTION  >> 
#
    if re.match("<<",CF) : 
      CF=re.sub("<<","",CF) 
      print("<form action=\"{0:s}\" method=\"post\">".format(CF)) 
      CF = ""
    if re.search(">>$",CF) : 
      CF=re.sub(">>","",CF) 
      print("</form>")  ; CF = ""
#
#	Tables	{{ || :: }}
#
    if re.match("{{{*",CF) : 
      TL=len(CF)-2 ; CF = "" ; TABL = 1
      print("<table class=\"formatter_table\" border=\"{0:d}\"><td class=\"formatter_table\">".format(TL))
    if re.match("[|][|]",CF) : print("<td class=\"formatter_table\">") ; CF=""
    if re.match("::",CF) : print("<tr>") ; CF=""
    if re.match("}}",CF) : print("</table>") ; CF="" ; TABL = 0
#
#	Ordered list
#
    if CF == "*" :
      if UL < 1 : print("<ul>") ; UL = 1
      print("<li>") ; CF="" ; UL = UL + 1
#
#	Unordered list
#
    if CF == "#" :
      if OL < 1 : print("<ol>") ; OL = 1
      print("<li>") ; CF="" ; OL = OL + 1
#
#	Rules, breaks and headings
#
    if re.match("----*",CF) : print("<hr>") ; CF = "" 	# Rule
    if re.match("%",CF) : print("<br>") ; CF = "" 	# Break
    if CF == "+" : print("<h1>") ; CF = "" ; H = 1	# Headings
    if CF == "++" : print("<h2>") ; CF = "" ; H = 2
    if CF == "+++" : print("<h3>") ; CF = "" ; H = 3
    if CF == "++++" : print("<h4>") ; CF = "" ; H = 4
#
#	Page links	[[[
#
    if re.match("\[\[\[",CF) : 
      CF=re.sub("\]\]\]","",CF)
      CF=re.sub("\[\[\[","",CF)
      LF=re.sub("\\.","",CF)
      print("<a href=\"wawki.cgi?{0:s}\">{1:s}</a>".format(LF,CF))
      CF = ""
#
#	Code		[[code]]
#
    if re.match("\[\[code\]\]",CF) :
      print("<pre class=\"formatter_pre\">") ; CF=""
    if re.match("\[\[/code\]\]",CF) :
      print("</pre>") ; CF=""
#
#	Image Links	[[
#
    if re.match("\[\[http://",CF) :
      IMG=re.sub("\[\[","",CF) ; CF = ""
    if re.search("\]\]$",CF) :
      CF=re.sub("\]\]$","",CF)
      if LAB != "" :
        LAB = LAB + " " + CF
      else :
        LAB = CF
      print("<img src=\"{0:s}\" border=\"0\" alt=\"{1:s}\">".format(IMG,LAB)) ; 
      IMG = "" ; LAB = "" ; CF = ""
    else :
      if IMG != "" : 
        LAB = CF ; CF = "" 
#
#	URL links	[
#
    if re.match("http://",CF) :
      print("<a href=\"{0:s}\">{0:s}</a>".format(CF,CF)) ; CF = "" 
    if re.match("\[http://",CF) :
      LINK=re.sub("\[","",CF) ; CF = ""
    if re.search("\]$",CF) :
      CF=re.sub("\]$","",CF)
      LAB = LAB + " " + CF
      print("<a href=\"{0:s}\">{1:s}</a>".format(LINK,LAB)) 
      LINK = "" ; LAB = "" ; CF = ""
    else :
      if LINK != "" : 
        LAB = CF ; CF = ""
#
#	Text modifiers
#
    if re.match("--[^-]",CF) : CF=re.sub("^--","<strike>",CF)
    if re.search("[^-]--$",CF) : CF=re.sub("--$","</strike>",CF)
    if re.match("__[^_]",CF) : CF=re.sub("^__","<u>",CF)
    if re.search("[^_]__$",CF) : CF=re.sub("__$","</u>",CF)
    if re.match("[*][*]",CF) : CF=re.sub("^[*][*]","<b>",CF)
    if re.search("[*][*]$",CF) : CF=re.sub("[*][*]$","</b>",CF)
    if re.match("//",CF) : CF=re.sub("^//","<i>",CF)
    if re.search("//$",CF) : CF=re.sub("//$","</i>",CF)
    if re.match("/[*]",CF) : CF=re.sub("^/[*]","<i><b>",CF)
    if re.search("[*]/$",CF) : CF=re.sub("[*]/$","</b></i>",CF)
    if re.search("[!]",CF) : CF=re.sub("[!]","",CF)	# Fake null	
    #print("{",CF,"}",)#end=' ')
    print(CF,end=' ')

  if H > 0 : print("</h{0:d}>".format(H)) ; H = 0
  if UL > 0 : 
    UL = UL - 1
    if UL == 0 : print("</ul>")
  if OL > 0 : 
    OL = OL - 1
    if OL == 0 : print("</ol>")
#
#  Process input file
#
def processFile(filename) :
  global current_line
  global current_sourceline
  directory = "."
  filepath = os.path.join(directory , filename)
  file = open(filepath, 'r') 
  for line in file :
    line = processLine(line)
  return
#
# Main program
#
def main() :
  global PAGE
  global DATE
  filename = None
  #print(sys.version)
  try :
    filename = sys.argv[1]
    PAGE = sys.argv[2]
    DATE = sys.argv[3]
  except IndexError :
    print("Usage: %s <FILENAME> <DATE>" % sys.argv[0])
    sys.exit(0)
  beginPage()
  processFile(filename)
  endPage()

main()

