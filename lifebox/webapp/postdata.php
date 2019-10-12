<?php
  $lifeboxfile = fopen("lifeboxdata", "w") or die("Unable to open file!");
  if (!is_numeric($_POST['amount-sp1-1'])) $_POST['amount-sp1-1']=512;
  if (!is_numeric($_POST['amount-sp1-2'])) $_POST['amount-sp1-2']=512;
  if (!is_numeric($_POST['amount-sp1-3'])) $_POST['amount-sp1-3']=512;
  if (!is_numeric($_POST['amount-sp1-4'])) $_POST['amount-sp1-4']=512;
  if (!is_numeric($_POST['amount-sp2-1'])) $_POST['amount-sp2-1']=512;
  if (!is_numeric($_POST['amount-sp2-2'])) $_POST['amount-sp2-2']=512;
  if (!is_numeric($_POST['amount-sp2-3'])) $_POST['amount-sp2-3']=512;
  if (!is_numeric($_POST['amount-sp2-4'])) $_POST['amount-sp2-4']=512;
  if (!is_numeric($_POST['amount-sp3-1'])) $_POST['amount-sp3-1']=512;
  if (!is_numeric($_POST['amount-sp3-2'])) $_POST['amount-sp3-2']=512;
  if (!is_numeric($_POST['amount-sp3-3'])) $_POST['amount-sp3-3']=512;
 

  $string =  $_POST['amount-sp3-1'] . "|" . $_POST['amount-sp3-2'] . "|" . $_POST['amount-sp3-3'] . "|" . $_POST['amount-sp1-2'] . "|" . $_POST['amount-sp1-1'] . "|" . $_POST['amount-sp1-3'] . "|" . $_POST['amount-sp1-4'] . "|" . $_POST['amount-sp2-1'] . "|" . $_POST['amount-sp2-2'] . "|" . $_POST['amount-sp2-3'] . "|" . $_POST['amount-sp2-4'];
  fwrite($lifeboxfile, $string);
  fclose($lifeboxfile);
?>
