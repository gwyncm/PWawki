#
# Wawki edit version 1.0 Copyright Gwyneth Morrison
#
BEGIN 	{ 
	printf("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2//EN\">\n");
	printf("<HTML><HEAD><title>%s</title></HEAD>\n",PAGE)
printf("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://gwynux.ca/css/formatter.css\" /></HEAD>\n");
	while (getline IR <"data/EditHeader" >0) print IR
	printf ("<form action=\"wawki.cgi?!%s" type "\" method=\"post\">",PAGE)
	print "<textarea name=textin cols=80 rows=25>"
	}
END	{
	print "</textarea><input type=submit value=\"Submit entry\"></form>"
	printf("<p><HR><a href=\"wawki.cgi?HomePage\">Home</a>\n")
	if ( EDIT == "1" ) printf("  <a href=\"wawki.cgi?@%s\">Edit</a>\n",PAGE)
	printf("  <a href=\"wawki.cgi?SysHelp\">Help</a>\n")
	printf("| Last Modified: %s \n",DATE)
	printf("<hr></BODY></HTML>\n")
	}
	{ 	# Just print each line
	printf ("%s\n", $0 ) 
	} 
