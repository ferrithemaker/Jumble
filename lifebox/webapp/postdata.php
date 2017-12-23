<?php
  $lifeboxfile = fopen("lifeboxdata", "w") or die("Unable to open file!");
  $string =  $_POST['vsp1-1'] . "|" . $_POST['vsp1-2'] . "|" . $_POST['vsp1-3'] . "|" . $_POST['vsp1-4'] . "|" . $_POST['vsp1-5'] . "|" . $_POST['vsp1-6'] . "|" . $_POST['vsp1-7'] . "|" . $_POST['vsp1-8'] . "|" . $_POST['vsp2-1'] . "|" . $_POST['vsp2-2'] . "|" . $_POST['vsp2-3'] . "|" . $_POST['vsp2-4'] . "|" . $_POST['vsp2-5'] . "|" . $_POST['vsp2-6'] . "|" . $_POST['vsp2-7'] . "|" . $_POST['vsp2-8'] . "|" . $_POST['vsp3-1'] . "|" . $_POST['vsp3-2'] . "|" . $_POST['vsp3-3'] . "|" . $_POST['vsp3-4'] . "|" . $_POST['vsp3-5'];
  fwrite($lifeboxfile, $string);
  fclose($lifeboxfile);
  header('Location: lifebox.php');
?>
