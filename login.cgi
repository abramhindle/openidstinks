#!/usr/bin/perl
use strict;
use CGI;
use Data::Dumper;
my $cgi = CGI->new();
print $cgi->header();
print Dumper($cgi->Vars());
