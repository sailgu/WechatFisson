use strict;
use warnings;
my $domain_list = shift @ARGV;

open my $IN, '<', $domain_list;
while(<$IN>){
    my $domain = (split)[0];
    my $reponse = `curl --connect-timeout 5 \'$domain\' 2>/dev/null`;
    print "$domain\n" if $reponse =~/weimob/;
}
