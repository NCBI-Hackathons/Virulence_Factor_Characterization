#!/usr/bin/env perl -w
#
#
use IO::All;
use feature 'say';
use Carp;
use strict;
use Data::Dumper;
use Array::Utils qw(:all);

my ($hmmOut1,$hmmOut2) = @ARGV;

# get the domains => key: domain; val: (ctg_id,full_evalue,aln_start,aln_end,#copies)
my %hmmOut1 = get_domains_info($hmmOut1); 
my %hmmOut2 = get_domains_info($hmmOut2);

#say Dumper \%hmmOut1;

# compare the two hashes
compare_metagenome(\%hmmOut1,\%hmmOut2);




# sub
sub compare_metagenome {

	my ($m1,$m2) = @_;
	
	my %m1 = %$m1;
	my %m2 = %$m2;

	# easiest way - do they have the same domains
	my @dom1 = (keys %m1);
	my @dom2 = (keys %m2);
	my @isect = intersect(@dom1, @dom2); # domains present in both datasets
	#print join(",", @isect) . "\n";
	my @diff = array_diff(@dom1, @dom2);
	my @unique = unique(@dom1,@dom2);
	
	warn"...\t# of domains found in the two datasets:\t". @isect ."\n";
	warn"...\t# of domains that are different\t". @diff ."\n";
	warn"...\t# of domains that are unique\t". @unique ."\n";
	
}
sub get_domains_info {
	my %h = ();
	my $f = io(@_);
	$f->autoclose(0);
	while(my $l = $f->getline || $f->getline){
	chomp $l;
		next if $l =~m/^#/;
		my @data = split /\s+/, $l;
		my ($target,$qry,$eval,$alnS,$alnE) = ($data[0],$data[3],$data[6],$data[19],$data[20]);	
		@{$h{$qry}} = ($target,$eval,$alnS,$alnE);
	}
	return(%h);
}

