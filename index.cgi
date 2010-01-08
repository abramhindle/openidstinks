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
		return $cgi->param('user') || $u || "lolhy";
		return $identity unless $u;
		return "http://churchturing.org/openid/index.cgi?user="."lolhy"
	},
	#get_identity => sub { $cgi->param('userid') || "lolhy" },
	is_identity  => sub {
		my ($u, $identity) = @_;
		return 1;
		return $u
	},
	is_trusted   => sub {
		my ($u,$trust_root,$id_identity) = @_;
		return 1;
		return $u
	},
	endpoint_url => "http://churchturing.org/openid/server.cgi",
	#setup_url => "http://churchturing.org/openid/index.cgi",
	setup_url => "http://churchturing.org/openid/server.cgi",
	server_secret => "balls",
);

my ($type, $data) = $nos->handle_page;
#warn "$type,$data";
warn "TYPE $type";
if ($type eq "redirect") {
        my $url = $nos->signed_return_url(
		identity      => $nos->args('openid.identity'),
		return_to     => $nos->args('openid.return_to'),
		assoc_handle  => $nos->args('openid.assoc_handle'),
		trust_root    => $nos->args('openid.trust_root'));
	$url =~ s/invalidate_handle/assoc_handle/; # Hack for Net::OpenID::Server.
	#print $cgi->redirect($url);
	print "Status: 301\n";
	print "Location: $url\n\n";
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
	print "Status: 301\n";
	print "Location: $url\n\n";

} else {
        # Hack for Net::OpenID::Server.
	if ($type eq 'text/plain' && $data =~ /^assoc_handle:\r?\n/s)
	{
		my $ahandle = 'assoc_handle:' . Net::OpenID::Server::rand_chars(10);
		$data =~ s/^assoc_handle:/$ahandle/e;
		$data =~ s/^expires_in:0/expires_in:3600/m;
	}
	warn "Sending $data";
	print "Content-Type: $type\n\n";
	print $data;
}
