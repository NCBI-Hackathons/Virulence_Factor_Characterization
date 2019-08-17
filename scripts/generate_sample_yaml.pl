#!/data/ousmane.cisse/conda/bin/perl -w
#
#
use IO::All;
use feature 'say';
use Carp;
use strict;
use Data::Dumper;

my $dir = io($ARGV[0]);
my @contents = @$dir;

say "samples:";
my $c = 1;

my $f = "";
foreach $f (@contents){
	if ($f =~ m/\.fasta/){
		say " G$c: $f";
		$c++;		
	}
}
