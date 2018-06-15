use utf8;  
use Encode;  
use URI::Escape;

$str = '%u6536%u6536%u6536';  
$str =~ s/%u([0-9a-fA-F]{4})/pack("U",hex($1))/eg;  
print "\n";
print $str, "未分组";  
print "\n";
print "\n";
$str = encode( "utf8", $str );  
print $str,  "未分组";  
print "\n";
