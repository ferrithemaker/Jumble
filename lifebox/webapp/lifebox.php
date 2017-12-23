<!doctype html>
<html lang="en">
<head>
  <?php
  $lifeboxfile = fopen("lifeboxdata", "r") or die("Unable to open file!");
  $lifeboxstring = fread($lifeboxfile,filesize("lifeboxdata"));
  fclose($lifeboxfile);
  $lifeboxarray = explode("|",$lifeboxstring);
  ?>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LifeBox Manager</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script>
  $( function() {
    $( "#tabs" ).tabs();
  } );
  </script>
<script>
  $( function() {
    $( "#sp1-1" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[0]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-1" ).val( ui.value );
      }
    });
    $( "#sp1-2" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[1]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-2" ).val( ui.value );
      }
    });
    $( "#sp1-3" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[2]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-3" ).val( ui.value );
      }
    });
    $( "#sp1-4" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[3]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-4" ).val( ui.value );
      }
    });
    $( "#sp1-5" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[4]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-5" ).val( ui.value );
      }
    });
    $( "#sp1-6" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[5]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-6" ).val( ui.value );
      }
    });
    $( "#sp1-7" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[6]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-7" ).val( ui.value );
      }
    });
    $( "#sp1-8" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[7]?>,
      slide: function( event, ui ) {
        $( "#amount-sp1-8" ).val( ui.value );
      }
    });
    
    $( "#sp2-1" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[8]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-1" ).val( ui.value );
      }
    });
    $( "#sp2-2" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[9]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-2" ).val( ui.value );
      }
    });
    $( "#sp2-3" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[10]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-3" ).val( ui.value );
      }
    });
    $( "#sp2-4" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[11]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-4" ).val( ui.value );
      }
    });
    $( "#sp2-5" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[12]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-5" ).val( ui.value );
      }
    });
    $( "#sp2-6" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[13]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-6" ).val( ui.value );
      }
    });
    $( "#sp2-7" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[14]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-7" ).val( ui.value );
      }
    });
    $( "#sp2-8" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[15]?>,
      slide: function( event, ui ) {
        $( "#amount-sp2-8" ).val( ui.value );
      }
    });
    
    $( "#sp3-1" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[16]?>,
      slide: function( event, ui ) {
        $( "#amount-sp3-1" ).val( ui.value );
      }
    });
    $( "#sp3-2" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[17]?>,
      slide: function( event, ui ) {
        $( "#amount-sp3-2" ).val( ui.value );
      }
    });
    $( "#sp3-3" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[18]?>,
      slide: function( event, ui ) {
        $( "#amount-sp3-3" ).val( ui.value );
      }
    });
    $( "#sp3-4" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[19]?>,
      slide: function( event, ui ) {
        $( "#amount-sp3-4" ).val( ui.value );
      }
    });
    $( "#sp3-5" ).slider({
      range: "min",
      min: 0,
      max: 100,
      value: <?=$lifeboxarray[20]?>,
      slide: function( event, ui ) {
        $( "#amount-sp3-5" ).val( ui.value );
      }
    });
    
    $( "#amount-sp1-1" ).val( $( "#sp1-1" ).slider( "value" ) );
    $( "#amount-sp1-2" ).val( $( "#sp1-2" ).slider( "value" ) );
    $( "#amount-sp1-3" ).val( $( "#sp1-3" ).slider( "value" ) );
    $( "#amount-sp1-4" ).val( $( "#sp1-4" ).slider( "value" ) );
    $( "#amount-sp1-5" ).val( $( "#sp1-5" ).slider( "value" ) );
    $( "#amount-sp1-6" ).val( $( "#sp1-6" ).slider( "value" ) );
    $( "#amount-sp1-7" ).val( $( "#sp1-7" ).slider( "value" ) );
    $( "#amount-sp1-8" ).val( $( "#sp1-8" ).slider( "value" ) );
    
    $( "#amount-sp2-1" ).val( $( "#sp2-1" ).slider( "value" ) );
    $( "#amount-sp2-2" ).val( $( "#sp2-2" ).slider( "value" ) );
    $( "#amount-sp2-3" ).val( $( "#sp2-3" ).slider( "value" ) );
    $( "#amount-sp2-4" ).val( $( "#sp2-4" ).slider( "value" ) );
    $( "#amount-sp2-5" ).val( $( "#sp2-5" ).slider( "value" ) );
    $( "#amount-sp2-6" ).val( $( "#sp2-6" ).slider( "value" ) );
    $( "#amount-sp2-7" ).val( $( "#sp2-7" ).slider( "value" ) );
    $( "#amount-sp2-8" ).val( $( "#sp2-8" ).slider( "value" ) );
    
    $( "#amount-sp3-1" ).val( $( "#sp3-1" ).slider( "value" ) );
    $( "#amount-sp3-2" ).val( $( "#sp3-2" ).slider( "value" ) );
    $( "#amount-sp3-3" ).val( $( "#sp3-3" ).slider( "value" ) );
    $( "#amount-sp3-4" ).val( $( "#sp3-4" ).slider( "value" ) );
    $( "#amount-sp3-5" ).val( $( "#sp3-5" ).slider( "value" ) );
  } );
  
  function AddPostData(){

	var formInfo = document.forms['lifeboxform'];

	formInfo.elements["vsp1-1"].value = $( "#sp1-1" ).slider( "value" );
	formInfo.elements["vsp1-2"].value = $( "#sp1-2" ).slider( "value" );
	formInfo.elements["vsp1-3"].value = $( "#sp1-3" ).slider( "value" );
	formInfo.elements["vsp1-4"].value = $( "#sp1-4" ).slider( "value" );
	formInfo.elements["vsp1-5"].value = $( "#sp1-5" ).slider( "value" );
	formInfo.elements["vsp1-6"].value = $( "#sp1-6" ).slider( "value" );
	formInfo.elements["vsp1-7"].value = $( "#sp1-7" ).slider( "value" );
	formInfo.elements["vsp1-8"].value = $( "#sp1-8" ).slider( "value" );
	
	formInfo.elements["vsp2-1"].value = $( "#sp2-1" ).slider( "value" );
	formInfo.elements["vsp2-2"].value = $( "#sp2-2" ).slider( "value" );
	formInfo.elements["vsp2-3"].value = $( "#sp2-3" ).slider( "value" );
	formInfo.elements["vsp2-4"].value = $( "#sp2-4" ).slider( "value" );
	formInfo.elements["vsp2-5"].value = $( "#sp2-5" ).slider( "value" );
	formInfo.elements["vsp2-6"].value = $( "#sp2-6" ).slider( "value" );
	formInfo.elements["vsp2-7"].value = $( "#sp2-7" ).slider( "value" );
	formInfo.elements["vsp2-8"].value = $( "#sp2-8" ).slider( "value" );
	
	formInfo.elements["vsp3-1"].value = $( "#sp3-1" ).slider( "value" );
	formInfo.elements["vsp3-2"].value = $( "#sp3-2" ).slider( "value" );
	formInfo.elements["vsp3-3"].value = $( "#sp3-3" ).slider( "value" );
	formInfo.elements["vsp3-4"].value = $( "#sp3-4" ).slider( "value" );
	formInfo.elements["vsp3-5"].value = $( "#sp3-5" ).slider( "value" );
	
	
	//console.log(formInfo.elements["vsp1-1"].value);

  }
  </script>
</head>
<body>
 
<div id="tabs">
  <ul>
    <li><a href="#tabs-1">Specie 1 (yellow)</a></li>
    <li><a href="#tabs-2">Specie 2 (blue)</a></li>
    <li><a href="#tabs-3">Mana (white)</a></li>
  </ul>
  <div id="tabs-1">
    <p>
  	<label for="amount-sp1-1">LIFE_EXPECTANCY:</label>
  	<p>Life expectancy is a statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.</p>
  	<input type="text" id="amount-sp1-1" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-1"></div>
    <p>
  	<label for="amount-sp1-2">NEARBORN_CHANCES:</label>
  	<p>When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.</p>
  	<input type="text" id="amount-sp1-2" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-2"></div>
    <p>
  	<label for="amount-sp1-3">RANDOM_BORN_CHANCES:</label>
  	<p>Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
    Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
    </p>
  	<input type="text" id="amount-sp1-3" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-3"></div>
    <p>
  	<label for="amount-sp1-4">DIE_CHANCES:</label>
  	<p>As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time. 
    </p>
  	<input type="text" id="amount-sp1-4" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-4"></div>
    <p>
  	<label for="amount-sp1-5">ENERGY_BASE:</label>
  	<input type="text" id="amount-sp1-5" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-5"></div>
    <p>
  	<label for="amount-sp1-6">ENERGY_NEEDED_PER_CYCLE:</label>
  	<input type="text" id="amount-sp1-6" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-6"></div>
    <p>
  	<label for="amount-sp1-7">MAX_ENERGY_RECOLECTED_PER_CYCLE:</label>
  	<input type="text" id="amount-sp1-7" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-7"></div>
    <p>
  	<label for="amount-sp1-8">ENERGY_TO_REPLICATE:</label>
  	<input type="text" id="amount-sp1-8" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp1-8"></div>
  </div>
  <div id="tabs-2">
	<p>
  	<label for="amount-sp2-1">LIFE_EXPECTANCY:</label>
  	<p>Life expectancy is a statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.</p>
  	<input type="text" id="amount-sp2-1" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-1"></div>
    <p>
  	<label for="amount-sp2-2">NEARBORN_CHANCES:</label>
  	<p>When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.</p>
  	<input type="text" id="amount-sp2-2" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-2"></div>
    <p>
  	<label for="amount-sp2-3">RANDOM_BORN_CHANCES:</label>
  	<p>Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
    Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
    </p>
  	<input type="text" id="amount-sp2-3" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-3"></div>
    <p>
  	<label for="amount-sp2-4">DIE_CHANCES:</label>
  	<p>As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time. 
    </p>
  	<input type="text" id="amount-sp2-4" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-4"></div>
    <p>
  	<label for="amount-sp2-5">ENERGY_BASE:</label>
  	<input type="text" id="amount-sp2-5" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-5"></div>
    <p>
  	<label for="amount-sp2-6">ENERGY_NEEDED_PER_CYCLE:</label>
  	<input type="text" id="amount-sp2-6" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-6"></div>
    <p>
  	<label for="amount-sp2-7">MAX_ENERGY_RECOLECTED_PER_CYCLE:</label>
  	<input type="text" id="amount-sp2-7" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-7"></div>
    <p>
  	<label for="amount-sp2-8">ENERGY_TO_REPLICATE:</label>
  	<input type="text" id="amount-sp2-8" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp2-8"></div>
  </div>
  <div id="tabs-3">
	<p>
  	<label for="amount-sp3-1">LIFE_EXPECTANCY:</label>
  	<p>Life expectancy is a statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.</p>
  	<input type="text" id="amount-sp3-1" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp3-1"></div>
    <p>
  	<label for="amount-sp3-2">NEARBORN_CHANCES:</label>
  	<p>When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.</p>
  	<input type="text" id="amount-sp3-2" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp3-2"></div>
    <p>
  	<label for="amount-sp3-3">RANDOM_BORN_CHANCES:</label>
  	<p>Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
    Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
    </p>
  	<input type="text" id="amount-sp3-3" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp3-3"></div>
    <p>
  	<label for="amount-sp3-4">DIE_CHANCES:</label>
  	<p>As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time. 
    </p>
  	<input type="text" id="amount-sp3-4" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp3-4"></div>
    <p>
  	<label for="amount-sp3-5">ENERGY_GENERATION_PER_CYCLE:</label>
  	<input type="text" id="amount-sp3-5" readonly style="border:0; color:#f6931f; font-weight:bold;">
    </p>
    <div id="sp3-5"></div>
  </div>
</div>
<div style="margin-top:50px">
<form id="lifeboxform" action="postdata.php" method="POST" onsubmit="return AddPostData()">
<input type="submit" style="width: 20em;  height: 2em;" value="Update LifeBox values">

<input type="hidden" name="vsp1-1" value=""/>
<input type="hidden" name="vsp1-2" value=""/>
<input type="hidden" name="vsp1-3" value=""/>
<input type="hidden" name="vsp1-4" value=""/>
<input type="hidden" name="vsp1-5" value=""/>
<input type="hidden" name="vsp1-6" value=""/>
<input type="hidden" name="vsp1-7" value=""/>
<input type="hidden" name="vsp1-8" value=""/>

<input type="hidden" name="vsp2-1" value=""/>
<input type="hidden" name="vsp2-2" value=""/>
<input type="hidden" name="vsp2-3" value=""/>
<input type="hidden" name="vsp2-4" value=""/>
<input type="hidden" name="vsp2-5" value=""/>
<input type="hidden" name="vsp2-6" value=""/>
<input type="hidden" name="vsp2-7" value=""/>
<input type="hidden" name="vsp2-8" value=""/>

<input type="hidden" name="vsp3-1" value=""/>
<input type="hidden" name="vsp3-2" value=""/>
<input type="hidden" name="vsp3-3" value=""/>
<input type="hidden" name="vsp3-4" value=""/>
<input type="hidden" name="vsp3-5" value=""/>

</form>
</div>
 
 
</body>
</html>
