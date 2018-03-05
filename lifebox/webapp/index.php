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
  <script src="jquery.knob.min.js"></script>
  <script>
	$(function($) {

		$(".knob").knob({
			change : function (value) {
				//console.log("change : " + value);
				
			},
			release : function (value) {
				
				console.log(this.$.attr('id'));
				console.log(this);
				console.log("release : " + value);
				console.log($("#amount-sp1-1").val());
				$.ajax({
					type: 'POST',
					cache: false,
					url: './postdata.php',
					data: 'amount-sp1-1='+$("#amount-sp1-1").val()+
						  '&amount-sp1-2='+$("#amount-sp1-2").val()+
						  '&amount-sp1-3='+$("#amount-sp1-3").val()+
						  '&amount-sp1-4='+$("#amount-sp1-4").val()+
						  '&amount-sp1-5='+$("#amount-sp1-5").val()+
						  '&amount-sp1-6='+$("#amount-sp1-6").val()+
						  '&amount-sp1-7='+$("#amount-sp1-7").val()+
						  '&amount-sp1-8='+$("#amount-sp1-8").val()+
						  '&amount-sp2-1='+$("#amount-sp2-1").val()+
						  '&amount-sp2-2='+$("#amount-sp2-2").val()+
						  '&amount-sp2-3='+$("#amount-sp2-3").val()+
						  '&amount-sp2-4='+$("#amount-sp2-4").val()+
						  '&amount-sp2-5='+$("#amount-sp2-5").val()+
						  '&amount-sp2-6='+$("#amount-sp2-6").val()+
						  '&amount-sp2-7='+$("#amount-sp2-7").val()+
						  '&amount-sp2-8='+$("#amount-sp2-8").val()+
						  '&amount-sp3-1='+$("#amount-sp3-1").val()+
						  '&amount-sp3-2='+$("#amount-sp3-2").val()+
						  '&amount-sp3-3='+$("#amount-sp3-3").val()+
						  '&amount-sp3-4='+$("#amount-sp3-4").val()+
						  '&amount-sp3-5='+$("#amount-sp3-5").val()
					, 
					//success: function(msg) {
					//	$("#boxContentId").html(msg);
					//}
				});
				
			},
			cancel : function () {
				console.log("cancel : ", this);
			},
			/*format : function (value) {
			 return value + '%';
			 },*/
			draw : function () {

				// "tron" case
				if(this.$.data('skin') == 'tron') {

					this.cursorExt = 0.3;

					var a = this.arc(this.cv)  // Arc
							, pa                   // Previous arc
							, r = 1;

					this.g.lineWidth = this.lineWidth;

					if (this.o.displayPrevious) {
						pa = this.arc(this.v);
						this.g.beginPath();
						this.g.strokeStyle = this.pColor;
						this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, pa.s, pa.e, pa.d);
						this.g.stroke();
					}

					this.g.beginPath();
					this.g.strokeStyle = r ? this.o.fgColor : this.fgColor ;
					this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, a.s, a.e, a.d);
					this.g.stroke();

					this.g.lineWidth = 2;
					this.g.beginPath();
					this.g.strokeStyle = this.o.fgColor;
					this.g.arc( this.xy, this.xy, this.radius - this.lineWidth + 1 + this.lineWidth * 2 / 3, 0, 2 * Math.PI, false);
					this.g.stroke();

					return false;
				}
			}
		});

		// Example of infinite knob, iPod click wheel
		var v, up=0,down=0,i=0
				,$idir = $("div.idir")
				,$ival = $("div.ival")
				,incr = function() { i++; $idir.show().html("+").fadeOut(); $ival.html(i); }
				,decr = function() { i--; $idir.show().html("-").fadeOut(); $ival.html(i); };
		$("input.infinite").knob(
				{
					min : 0
					, max : 20
					, stopper : false
					, change : function () {
					if(v > this.cv){
						if(up){
							decr();
							up=0;
						}else{up=1;down=0;}
					} else {
						if(v < this.cv){
							if(down){
								incr();
								down=0;
							}else{down=1;up=0;}
						}
					}
					v = this.cv;
				}
				});
	});
  </script>
  <script>
  $( function() {
    $( "#tabs" ).tabs();
  } );
  </script>

</head>
<body>
<form id="lifeboxform" action="postdata.php" method="POST">
<div id="tabs">
  <ul style="background: white;">
    <li style="background: lightblue;"><a href="#tabs-1">Specie 1 (yellow)</a></li>
    <li style="background: lightblue;"><a href="#tabs-2">Specie 2 (blue)</a></li>
    <li style="background: lightblue;"><a href="#tabs-3">Mana (white)</a></li>
  </ul>
  <div id="tabs-1">
    <p>
  	<label for="amount-sp1-1">LIFE_EXPECTANCY:</label>
  	<p>Life expectancy is a statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.</p>
  	<input class="knob" id="amount-sp1-1" name="amount-sp1-1" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[0]?>">
    </p>
    <div id="sp1-1"></div>
    <p>
  	<label for="amount-sp1-2">NEARBORN_CHANCES:</label>
  	<p>When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.</p>
  	<input class="knob" id="amount-sp1-2" name="amount-sp1-2" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[1]?>">
    </p>
    <div id="sp1-2"></div>
    <p>
  	<label for="amount-sp1-3">RANDOM_BORN_CHANCES:</label>
  	<p>Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
    Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
    </p>
	<input class="knob" id="amount-sp1-3" name="amount-sp1-3" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[2]?>">
    </p>
    <div id="sp1-3"></div>
    <p>
  	<label for="amount-sp1-4">DIE_CHANCES:</label>
  	<p>As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time. 
    </p>
    <input class="knob" id="amount-sp1-4" name="amount-sp1-4" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[3]?>">
	</p>
    <div id="sp1-4"></div>
    <p>
  	<label for="amount-sp1-5">ENERGY_BASE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp1-5" name="amount-sp1-5" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[4]?>">
    </p>
    <div id="sp1-5"></div>
    <p>
  	<label for="amount-sp1-6">ENERGY_NEEDED_PER_CYCLE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp1-6" name="amount-sp1-6" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[5]?>">
    </p>
    <div id="sp1-6"></div>
    <p>
  	<label for="amount-sp1-7">MAX_ENERGY_RECOLECTED_PER_CYCLE:</label>
  	<p>Falta descripcio</p>
	<input class="knob" id="amount-sp1-7" name="amount-sp1-7" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[6]?>">
	</p>
    <div id="sp1-7"></div>
    <p>
  	<label for="amount-sp1-8">ENERGY_TO_REPLICATE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp1-8" name="amount-sp1-8" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[7]?>">
    </p>
    <div id="sp1-8"></div>
  </div>
  <div id="tabs-2">
	<p>
  	<label for="amount-sp2-1">LIFE_EXPECTANCY:</label>
  	<p>Life expectancy is a statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.</p>
  	<input class="knob" id="amount-sp2-1" name="amount-sp2-1" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[8]?>">
    </p>
    <div id="sp2-1"></div>
    <p>
  	<label for="amount-sp2-2">NEARBORN_CHANCES:</label>
  	<p>When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.</p>
  	<input class="knob" id="amount-sp2-2" name="amount-sp2-2" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[9]?>">
    </p>
    <div id="sp2-2"></div>
    <p>
  	<label for="amount-sp2-3">RANDOM_BORN_CHANCES:</label>
  	<p>Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
    Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
    </p>
  	<input class="knob" id="amount-sp2-3" name="amount-sp2-3" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[10]?>">
    </p>
    <div id="sp2-3"></div>
    <p>
  	<label for="amount-sp2-4">DIE_CHANCES:</label>
  	<p>As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time. 
    </p>
  	<input class="knob" id="amount-sp2-4" name="amount-sp2-4" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[11]?>">
    </p>
    <div id="sp2-4"></div>
    <p>
  	<label for="amount-sp2-5">ENERGY_BASE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp2-5" name="amount-sp2-5" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[12]?>">
    </p>
    <div id="sp2-5"></div>
    <p>
  	<label for="amount-sp2-6">ENERGY_NEEDED_PER_CYCLE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp2-6" name="amount-sp2-6" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[13]?>">
    </p>
    <div id="sp2-6"></div>
    <p>
  	<label for="amount-sp2-7">MAX_ENERGY_RECOLECTED_PER_CYCLE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp2-7" name="amount-sp2-7" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[14]?>">
    </p>
    <div id="sp2-7"></div>
    <p>
  	<label for="amount-sp2-8">ENERGY_TO_REPLICATE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp2-8" name="amount-sp2-8" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[15]?>">
    </p>
    <div id="sp2-8"></div>
  </div>
  <div id="tabs-3">
	<p>
  	<label for="amount-sp3-1">LIFE_EXPECTANCY:</label>
  	<p>Life expectancy is a statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.</p>
  	<input class="knob" id="amount-sp3-1" name="amount-sp3-1" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[16]?>">
    </p>
    <div id="sp3-1"></div>
    <p>
  	<label for="amount-sp3-2">NEARBORN_CHANCES:</label>
  	<p>When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.</p>
  	<input class="knob" id="amount-sp3-2" name="amount-sp3-2" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[17]?>">
    </p>
    <div id="sp3-2"></div>
    <p>
  	<label for="amount-sp3-3">RANDOM_BORN_CHANCES:</label>
  	<p>Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
    Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
    </p>
  	<input class="knob" id="amount-sp3-3" name="amount-sp3-3" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[18]?>">
    </p>
    <div id="sp3-3"></div>
    <p>
  	<label for="amount-sp3-4">DIE_CHANCES:</label>
  	<p>As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time. 
    </p>
  	<input class="knob" id="amount-sp3-4" name="amount-sp3-4" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[19]?>">
    </p>
    <div id="sp3-4"></div>
    <p>
  	<label for="amount-sp3-5">ENERGY_GENERATION_PER_CYCLE:</label>
  	<p>Falta descripcio</p>
  	<input class="knob" id="amount-sp3-5" name="amount-sp3-5" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[20]?>">
    </p>
    <div id="sp3-5"></div>
  </div>
</div>
</form>
</div>
 
 
</body>
</html>
