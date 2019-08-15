#!/usr/bin/env perl -w
#
use IO::All;
use feature 'say';
use Carp;
use strict;
use Data::Dumper;

my ($info,$fasta) = @ARGV; 

# parse the info file and retrieve the header, so I can extract the fasta
my %genes = (); 

my $fi = io($info);
$fi->autoclose(0);
while(my $l = $fi->getline || $fi->getline){
chomp $l;
	my @data = split /\t/, $l;
	my ($gene,$species) = @data[0..1];

	# retrieve original headers
	my @species = split /,/, $species;
        my @headers = ();
	my $sp = "";
	foreach $sp (@species){
		my $header = get_header($gene,$sp,$fasta);
		push(@headers, $header);
	}       
	@{$genes{$gene}} = @headers;
}
say Dumper \%genes;

# dumping the gene in a file and run seqtk on it to get the fasta
my $buf = "";
my @all_tmp = ();
my $i = "";
foreach $i (keys %genes){
	my @hds = @{$genes{$i}};
	my @nr = uniq(@hds);
       	my $id2 = "";
	foreach $id2 (@nr){
		$buf .="$id2\n";
	}
	$i =~s/\(|\)//g;
	io("$info.$i.tmp")->write($buf);
	push(@all_tmp,"$info.$i.tmp");
}

# now run setk
my $t = ""; 
foreach $t (@all_tmp){
	my $cmd = "seqtk subseq $fasta $t > $t.fasta";
	run($cmd);
	my $cmd2 = "muscle -in $t.fasta -out $t.aln";
	run($cmd2);
	my $cmd3 = "perl /home/ousmane.cisse/DATA/NCBI_hack/scripts/fasta2stockholm.pl $t.aln > $t.sto";
        run($cmd3);
 	my $cmd4 = "hmmbuild $t.hmm $t.sto";	
	run($cmd4);
}

# 
sub get_header {
	my ($gne,$tofind,$fas) = @_;

	    $tofind =~s/-/ /g;
	my $f = io($fas);
	$f->autoclose(0);
	while(my $l = $f->getline || $f->getline){
	chomp $l;
		if (($l =~ m/$gne/) && ($l =~ m/$tofind/)){
			my @tmp = split /\s/, $l;
			$tmp[0] =~s/>//;
			return($tmp[0]);
		}
	}
}
sub run {
	my ($cmd) = @_;
	system($cmd)==0 || die "cannot run $cmd:$!\n";

}
sub uniq {
	my %seen;
	grep !$seen{$_}++, @_;
}
