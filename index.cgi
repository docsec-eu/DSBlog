#!/usr/local/bin/perl
use CGI;
use strict;

if (-e "./pwd") {
    print "Content-type:text/html\r\n\r\n";
    print "<html lang=\"en\"><meta charset=\"utf-8\">\n";
    print "<head>\n";
    print "<title>Blog</title>\n";
    print "</head>\n<body><h2><a href=\"?\" style=\"text-decoration:none;color:black\">Blog</a></h2>";
    print "<b>This is your sub title where you can describe what the blog is all about...</b>\n";
    print "<p style=\"text-align:right\">Here you can put your contact info:  <a href=\"mailto:bloguser\">E-Mail</a><p>\n";
    my $cgi = new CGI();
    my $maxtime = 2147483647;
    my $time_now = time();
    my $ts = sprintf("%X", ($maxtime - $time_now));
    my $linkstr = "";
    if ($cgi->param("ts")) {
        $ts = $cgi->param('ts');
    }
    $time_now = $maxtime - hex($ts);
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time_now);
    if ($cgi->param("y")) {
	$year =$cgi->param('y');	
    }
    my $this_year = 1900+ $year;
    if ($cgi->param("m")) {
	$mon = $cgi->param('m');
    }
    if ($mon <10) {
                $mon = "0".$mon;
    }
    if ($mday <10) {
                $mday = "0".$mday;
    }
    if ($cgi->param("a")) { ###
	open (PWDFILE, "<./pwd");	
	my $realpasswd =<PWDFILE>;
	chomp $realpasswd; 
	close (PWDFILE);
 	my $pwd=$cgi->param("a");
	if ($pwd ==$realpasswd) {
		$linkstr = "a=$pwd&";
		print "<h1>Welcome, Admin! <a href=\"?".$linkstr."e=New\"> create new logentry</a></h3>";
		my $entry="";
		if ($cgi->param('e')) {   #### insert entry
			$entry = $cgi->param('e');	
		        if (!(-d $this_year)) {
        		        mkdir ($this_year);
		        }
		        if (!(-d "$this_year/$mon")) {
	        	        mkdir ("$this_year/$mon");
		        }
		        if (!(-d "$this_year/$mon/$mday")) {
	        	        mkdir ("$this_year/$mon/$mday");
		        }
                        open (LOGENTRY, ">$this_year/$mon/$mday/$ts") or die "Could not open file $!";
                    	print LOGENTRY $entry;
                    	close (LOGENTRY);
		}
		if ($cgi->param('ts')) {
		        print "<h2>".DateStamp ($ts)."</h2>";
			print "<ul><li><a href=\"/?".$linkstr."ts=$ts\">[l]</a> ";
			ListEntry ("$this_year/$mon/$mday/$ts", 0);
   			print "</ul><h3>Edit:</h3><form action=\"/\" method=\"POST\"><textarea cols=\"80\" rows=\"10\" name=\"e\">";
			ListEntry ("$this_year/$mon/$mday/$ts", 0);		
			print "</textarea><br/><input type=\"hidden\" value=\"$pwd\" name=\"a\">";
			print "<input type=\"hidden\" value=\"$ts\" name=\"ts\">";
			print "<input type=\"submit\" value=\"Submit\"></form>";
		}
	} else { ## Not authorized 
	} 
    }
    elsif ($cgi->param('ts')) {
	my $ts = $cgi->param('ts');
	print "<h2>".DateStamp($ts)."</h2><ul>";	
	my $maxtime = 2147483647;
    	my $time_n = $maxtime - hex($ts);
    	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time_n);
    	my $this_year = 1900+ $year;
    	if ($mon <10) {
                $mon = "0".$mon;
    	}
    	if ($mday <10) {
                $mday = "0".$mday;
    	}
	ListEntryPlus ("./$this_year/$mon/$mday/", 0,$ts,$linkstr);
    } else {

       	ListBlog ($this_year, $mon, $linkstr);
    }
} else { #### No pwd file
	print "Content-type:text/html\r\n\r\n<html lang=\"en\"><meta charset=\"utf-8\">\n<body><h2>This blog seems unconfigured, please contact the administrator!</h2></body></html>";
	exit;
}

sub TimeStamp {
    my $timestamp = shift;
    my $maxtime = 2147483647;
    my $time_n = $maxtime - hex($timestamp);
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time_n);
    return ("$hour:$min.$sec");
}

sub DateStamp {
    my $timestamp = shift;
    my $maxtime = 2147483647;
    my @months = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
    my @days = qw(Sun Mon Tue Wed Thu Fri Sat Sun);
    my $time_n = $maxtime - hex($timestamp);
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time_n);
    my $this_year = 1900+ $year;
    return ("$days[$wday] $months[$mon] $mday $this_year");

}
sub ListEntry {
	my $targetentry = shift;
	my $htmlencode = shift;
	open (BLOGENTRY, "<$targetentry") or die "Could not open file $targetentry $!";
	while (<BLOGENTRY>) { 
		if ($htmlencode) {
		  print to_html($_); 
		} else { print $_;}
	}
}

sub ListEntryPlus {
 my $directory = shift;
 my $tohtml = shift;
 my $fn = shift; 
 my $linkstr = shift;
 print "<li><a href=\"?".$linkstr."ts=".$fn."\" title=\"".TimeStamp($fn)."\">[l]</a> ";
 ListEntry ("$directory$fn", $tohtml);
}

sub ListBlog {
	my $year = shift;
        my $month= shift;
	my $linkstr = shift;
	opendir my $mydir, "./$year/$month/";
	my @dirs = sort { $b+0 <=> $a+0} grep {-d "./$year/$month/" && ! /^\.{1,2}$/} readdir($mydir);
	closedir ($mydir);
	foreach my $dir (@dirs) {
		opendir my $d, "./$year/$month/$dir" or die "Cannot open directory:  ./$year/$month/$dir $!";
		my @files = sort { hex($a) <=> hex($b) } grep {-d "./$year/$month/$dir/" && ! /^\.{1,2}$/} readdir $d;
		closedir $d;
		my @popfiles= @files;
		print "<h2>".DateStamp(pop(@popfiles))."</h2><ul>";
		foreach my $file (@files) {
			ListEntryPlus ("./$year/$month/$dir/", 0,"$file", $linkstr);	
		}
		print "</ul>";
	}
}
sub to_html {
	my $formtext = shift;
	$formtext =~ s/(&)/&amp;/g;
	$formtext =~ s/(\")/&quot;/g;
	$formtext =~ s/(\')/&apos;/g;
	$formtext =~ s/(>)/&gt;/g;
	$formtext =~ s/(<)/&lt;/g;
	$formtext =~ s/(ß)/&szlig;/g;
	$formtext =~ s/(ä)/&auml;/g;
	$formtext =~ s/(ö)/&ouml;/g;
	$formtext =~ s/(ü)/&uuml;/g;
	$formtext =~ s/(Ä)/&Auml;/g;
        $formtext =~ s/(Ö)/&Ouml;/g;
        $formtext =~ s/(Ü)/&Uuml;/g;
        $formtext =~ s/(\r)/<br>/g;
        $formtext =~ s/(\n)/<br\/>/g;
	$formtext =~ s/<br><br\/>/<br>/g;
	return ($formtext);
}
