<?php
if (isset($_GET['data'])) {
	if (strlen($_GET['data'])<50 && filesize("temp.log")<50000000) {
		file_put_contents("temp.log",$_GET['data']."\n",FILE_APPEND);
	}
}
?>

