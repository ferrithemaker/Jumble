<?php
  $lifeboxfile = fopen("lifeboxdata", "w") or die("Unable to open file!");
  $string =  $_POST['amount-sp1-1'] . "|" . $_POST['amount-sp1-2'] . "|" . $_POST['amount-sp1-3'] . "|" . $_POST['amount-sp1-4'] . "|" . $_POST['amount-sp1-5'] . "|" . $_POST['amount-sp1-6'] . "|" . $_POST['amount-sp1-7'] . "|" . $_POST['amount-sp1-8'] . "|" . $_POST['amount-sp2-1'] . "|" . $_POST['amount-sp2-2'] . "|" . $_POST['amount-sp2-3'] . "|" . $_POST['amount-sp2-4'] . "|" . $_POST['amount-sp2-5'] . "|" . $_POST['amount-sp2-6'] . "|" . $_POST['amount-sp2-7'] . "|" . $_POST['amount-sp2-8'] . "|" . $_POST['amount-sp3-1'] . "|" . $_POST['amount-sp3-2'] . "|" . $_POST['amount-sp3-3'] . "|" . $_POST['amount-sp3-4'] . "|" . $_POST['amount-sp3-5'];
  fwrite($lifeboxfile, $string);
  fclose($lifeboxfile);
  header('Location: index.php');
?>
