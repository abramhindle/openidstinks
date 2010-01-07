#!/usr/bin/perl
use strict;
use lib qw(./lib);
use CGI;
use Net::OpenID::Server;
use Data::Dumper;
my $cgi = CGI->new();
#warn Dumper($cgi);
my $nos = Net::OpenID::Server->new(
	get_args     => $cgi,
	post_args    => $cgi,
	get_user     => sub { my ($u) = @_; $u || $cgi->param('user') || "lolhy"},
	#get_user => sub { "lolhy" },
	get_identity => sub {
		my( $u, $identity ) = @_;
		return $identity unless $u;
		return "http://churchturing.org/openid/index.cgi?user="."lolhy"
	},
	#get_identity => sub { $cgi->param('userid') || "lolhy" },
	is_identity  => sub {
		my ($u, $identity) = @_;
		return $u
	},
	is_trusted   => sub {
		my ($u,$trust_root,$id_identity) = @_;
		return $u
	},
	endpoint_url => "http://churchturing.org/openid/server.cgi",
	#setup_url => "http://churchturing.org/openid/index.cgi",
	setup_url => "http://churchturing.org/openid/login.cgi",
	server_secret => "balls",
);

my ($type, $data) = $nos->handle_page;
#warn "$type,$data";
warn "TYPE $type";
if ($type eq "redirect") {
	print $cgi->redirect($data);
} elsif ($type eq "setup") {
	my %setup_opts = %$data;
	# ... show them setup page(s), with options from setup_map
	# it's then your job to redirect them at the end to "return_to"
	# (or whatever you've named it in setup_map)
	#print $cgi->header();
	#print Dumper(\%setup_opts);
	my @query = ();
	while (my ($key,$val) = each %setup_opts) {
		push @query , uri_encode($key)."=".uri_encode($val);
	}
	my $url = "http://churchturing.org/openid/login.cgi?".join("&",@query);
	warn $url;
	print $cgi->redirect($url);
} else {
	print $cgi->header(-type => $type);
	print $data;
	warn "Sending $data";
}
