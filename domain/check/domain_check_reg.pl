use strict;
use warnings;

open my $IN, '<', 'good_domain.txt';
while(<$IN>){
    my $domain = (split)[0];
    my $reponse = `curl --connect-timeout 5 \'$domain\' 2>/dev/null`;
    print "$domain\n" if $reponse =~/weimob/;
}
