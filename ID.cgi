#!/usr/bin/perl
use strict;
use CGI;
use URI::Escape;


my $cgi = CGI->new();
print $cgi->header();
my $user = $cgi->param('user') || "lolhy";
my $safeuser = uri_escape($user);
print <<EOM;
<html>
<head>
<link rel="openid.server" href="http://churchturing.org/openid/server.cgi?user=$safeuser"/>
</head>
<body>
</body>
</html>
EOM
