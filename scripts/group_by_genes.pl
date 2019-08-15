#!/usr/bin/env perl -w
#
use IO::All;
use feature 'say';
use Carp;
use strict;
use Data::Dumper;

my %genes2species = ();

my $fas = io($ARGV[0]); 
$fas->autoclose(0);
while(my $l = $fas->getline || $fas->getline){
chomp $l;
	if ($l =~ m/^>/){
		my @data = split /\s+/, $l;
		my $id = $data[1];
		my ($sp) = $l =~/\]\s+\[(.*)\]/;
		$sp =~s/\s+/-/g;
		if ($genes2species{$id}){
			my @old = @{$genes2species{$id}};
			push(@old, $sp);
			@{$genes2species{$id}} = @old;
		} else {
			my @old = ();
			push(@old, $sp);
			@{$genes2species{$id}} = @old;
		}
	} else {
		next;
	}
}

#say Dumper \%genes2species;
# Each gene group contains only or two species. This is not going work for hmms
# I need to select only genes that have at least 5 species ( 5 is arbitrary)

my %good_targets = get_relevant_genes(%genes2species); 
#say Dumper \%good_targets;
my $found = (keys %good_targets);
warn"...found\t$found\tmakers w more than 5 species/genus!\n";

warn"... now writing the file $ARGV[0].Selected_Genes_info.txt!\n";
# now writing the file for fasta prep
#my $buf = "";
my $gt = "";
foreach $gt (keys %good_targets){
	my @sp2 = @{$good_targets{$gt}};
	my $sp2 = join(",", @sp2);
#	$buf .="$gt\t$sp2\n";
	say "$gt\t$sp2";
}
#io("$ARGV[0].Selected_Genes_info.txt")->write($buf);

# sub
sub get_relevant_genes {
	
	my %data = @_;

	my %selected = (); 

	my $g = "";
	foreach $g (keys %data){
		my @ids = @{$data{$g}};
		# I going to take species not sub
		# 'Mycobacterium-tuberculosis-H37Rv', and ''Mycobacterium-smegmatis-str.-MC2-155', are all the same
		my @species = get_species(@ids);
	       if (@species > 5) {
		       # say "TEST\t@species";
			@{$selected{$g}} = @ids;
	       } else {
	       		# skip
	       }
	}
	return(%selected);
}

sub get_species {
	my %h = ();
	my @data2 = @_;
	my $p = "";
	foreach $p (@data2){
		my @dta3 = split /\-/, $p;
		#say "TEST\t$p\t$dta3[0]";
		$h{$dta3[0]} = $p;	
	}	
	my @nr = (keys %h);
	return(@nr);
}
