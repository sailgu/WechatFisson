use warnings;

&main($ARGV[0]);

sub main(){
    my $table = read_table(shift);
    add_info_in_table($table);
    add_info_in_table($table);
    add_info_in_table($table);
    my @firidx_group = ([6..8], [12..14], [18..20]);
    my @secidx_group = ([9..11], [15..17], [21..23]);

    print "$table->{head}\t查询状态\t一级域名封禁代码\t一级域名封禁描述\t查询状态\t二级域名封禁代码\t二级域名封禁描述\n";
    for my $line (@{$table->{body}}){
        for my $start_idx (6,9){
            my @det_idx = map{$start_idx+2 + 6*$_} (0..2);
            if (scalar(@$line)<24){warn("$line->[0] has some error @det_idx\n")}
            my ($unclear, $true_idx) = count(@$line[@det_idx]);
            @$line[cor_idx($start_idx, 0)] = @$line[cor_idx($start_idx, $true_idx)];
            if ($unclear){
                warn("$line->[0] $start_idx inconsistency\n");
            }
        }
        print join("\t", @$line[0..5]), "\t";
        print join("\t", @$line[6..11]), "\n";
    }

}

sub cor_idx(){
    my ($start, $true_idx) = @_;
    return map {$start+6*$true_idx+$_} (0..2)
}

sub count(){
    my (%cnt, %res);
    map {push @{$cnt{$_[$_]}}, $_} 0..$#_; 
    my @sorted = sort {scalar(@{$cnt{$b}}) <=> scalar(@{$cnt{$a}})} keys %cnt;
    my $unclear = @sorted > 1 ? 1 : 0;
    my $true_idx = $cnt{$sorted[0]}[0];
    return($unclear, $true_idx);
}


sub add_info_in_table(){
    my $table = shift;
    for my $line (@{$table->{body}}){
        my %fir_blocked_info = blocked_info($line->[0]);
        my %sec_blocked_info = blocked_info("asi2wfdlx78lzr.$line->[0]");
        push @{$line}, (map {$fir_blocked_info{$_}} ('status', 'code', 'msg'));
        push @{$line}, (map {$sec_blocked_info{$_}} ('status', 'code', 'msg'));
    }
}

sub blocked_info (){
    my $check_base = "http://check.api-export.com/api/checkdomain?".
        "key=235e48db60605d00dc64df889dca69e1&url=";
    my $res = `curl \'$check_base$_[0]\' 2>/dev/null`;
    $res =~ s/\\u([0-9a-fA-F]{4})/pack("U",hex($1))/eg;  
    $res=~s/:/,/g;
    $res=~tr/{}/()/;
    my %res = eval($res);
    return %res;
}

sub read_table(){
    my %table;
    open my $IN, shift;
    my $head = <$IN>;
    chomp $head;
    $table{head} = $head;
    while(<$IN>){
        chomp;
        push @{$table{body}}, [split("\t", $_)];
    }
    return \%table;
}
