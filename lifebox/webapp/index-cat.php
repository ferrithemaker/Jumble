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
  <title>LifeConvent Manager</title>
  <link rel="stylesheet" href="jquery-ui.css">
  <script src="jquery-1.12.4.js"></script>
  <script src="jquery-ui.js"></script>
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
    <li style="background: lightblue;"><a href="#tabs-1">Especie 1 (groc)</a></li>
    <li style="background: lightblue;"><a href="#tabs-2">Especie 2 (blau)</a></li>
    <li style="background: lightblue;"><a href="#tabs-3">Manà (blanc)</a></li>
  </ul>
  <div id="tabs-1">
    <p>
  	<label for="amount-sp1-1">ESPERANÇA DE VIDA:</label>
  	<p>L'esperança de vida és una mesura estadística del temps mitjà que s'espera que visqui un organisme. Una vegada que l'entitat pixèlica es converteix en estable, l'esperança de vida determina quantes iteracions sobreviu.</p>
  	<input class="knob" id="amount-sp1-1" name="amount-sp1-1" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[0]?>">
    </p>
    <div id="sp1-1"></div>
    <p>
  	<label for="amount-sp1-2">INDEX DE REPRODUCCIÓ:</label>
  	<p>Quan una entitat píxelica compleix els requisits definits, es poden reproduir a una cel·la adjacent. Aquesta variable determina les possibilitats de reproducció, de manera que un valor superior significa més probabilitats de sobreviure.</p>
  	<input class="knob" id="amount-sp1-2" name="amount-sp1-2" data-width="200" data-min="1" data-max="5000" value="<?=$lifeboxarray[1]?>">
    </p>
    <div id="sp1-2"></div>
    <p>
  	<label for="amount-sp1-3">NAIXAMENT ESPONTANI:</label>
  	<p>La partenogèsia és un tret rar entre espècies que els permet reproduir-se sense aparellar-se. Les espècies dins de LifeBox poden reproduir-se d'una manera similar. En cas que ho aconsegueixin, la descendència es poblarà a l'atzar dins de la graella. Establir aquesta variable amb un valor alt significa grans possibilitats de reproduir-se d'aquesta manera. En cas contrari, si l'usuari decideix reduir aquest valor, la partenogènesi és menys probable.</p>
	<input class="knob" id="amount-sp1-3" name="amount-sp1-3" data-width="200" data-min="1" data-max="20" value="<?=$lifeboxarray[2]?>">
    </p>
    <div id="sp1-3"></div>
    <p>
  	<label for="amount-sp1-5">ENERGIA BASE:</label>
  	<p>Totes les espècies tenen un nivell de base d'energia definit quan neix, aquest nivell base condiciona les possibilitats de supervivència en les primeres etapes de la seva vida.</p>
  	<input class="knob" id="amount-sp1-5" name="amount-sp1-5" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[4]?>">
    </p>
    <div id="sp1-5"></div>
    <p>
  	<label for="amount-sp1-6">EFICIÈNCIA CONSUM:</label>
  	<p>Aquest paràmetre defineix el consum d'energia en cada iteració. Els valors més alts fan que l'espècie necessiti més energia per cicle d'iteració, que significa menys eficiència.</p>
  	<input class="knob" id="amount-sp1-6" name="amount-sp1-6" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[5]?>">
    </p>
    <div id="sp1-6"></div>
    <p>
  	<label for="amount-sp1-7">EFICIÈNCIA RECOLLIDA:</label>
  	<p>D'igual manera que el paràmetre anterior defineix l'eficiència del consum energètic, aquest defineix l'eficiència de la recollida d'energia del manà. Els valors més alts impliquen més eficiència de recollida.</p>
	<input class="knob" id="amount-sp1-7" name="amount-sp1-7" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[6]?>">
	</p>
    <div id="sp1-7"></div>
    <p>
  	<label for="amount-sp1-8">ENERGIA MÍNIMA PER REPRODUIR-SE:</label>
  	<p>Per permetre la replicació d'espècies, cada individu necessita superar un llindar energètic, la quantitat mínima d'energia necessària per reproduir-se. Els valors més alts signifiquen un llindar superior.</p>
  	<input class="knob" id="amount-sp1-8" name="amount-sp1-8" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[7]?>">
    </p>
    <div id="sp1-8"></div>
  </div>
  <div id="tabs-2">
	<p>
  	<label for="amount-sp2-1">ESPERANÇA DE VIDA:</label>
  	<p>L'esperança de vida és una mesura estadística del temps mitjà que s'espera que visqui un organisme. Una vegada que l'entitat pixèlica es converteix en estable, l'esperança de vida determina quantes iteracions sobreviu.</p>
  	<input class="knob" id="amount-sp2-1" name="amount-sp2-1" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[8]?>">
    </p>
    <div id="sp2-1"></div>
    <p>
  	<label for="amount-sp2-2">INDEX DE REPRODUCCIÓ:</label>
	<p>Quan una entitat píxelica compleix els requisits definits, es poden reproduir a una cel·la adjacent. Aquesta variable determina les possibilitats de reproducció, de manera que un valor superior significa més probabilitats de sobreviure.</p>
  	<input class="knob" id="amount-sp2-2" name="amount-sp2-2" data-width="200" data-min="1" data-max="5000" value="<?=$lifeboxarray[9]?>">
    </p>
    <div id="sp2-2"></div>
    <p>
  	<label for="amount-sp2-3">NAIXAMENT ESPONTANI:</label>
  	<p>La partenogèsia és un tret rar entre espècies que els permet reproduir-se sense aparellar-se. Les espècies dins de LifeBox poden reproduir-se d'una manera similar. En cas que ho aconsegueixin, la descendència es poblarà a l'atzar dins de la graella. Establir aquesta variable amb un valor alt significa grans possibilitats de reproduir-se d'aquesta manera. En cas contrari, si l'usuari decideix reduir aquest valor, la partenogènesi és menys probable.</p>
  	<input class="knob" id="amount-sp2-3" name="amount-sp2-3" data-width="200" data-min="1" data-max="20" value="<?=$lifeboxarray[10]?>">
    </p>
    <div id="sp2-3"></div>
    <p>
  	<label for="amount-sp2-5">ENERGIA BASE:</label>
  	<p>Totes les espècies tenen un nivell de base d'energia definit quan neix, aquest nivell base condiciona les possibilitats de supervivència en les primeres etapes de la seva vida.</p>
  	<input class="knob" id="amount-sp2-5" name="amount-sp2-5" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[12]?>">
    </p>
    <div id="sp2-5"></div>
    <p>
  	<label for="amount-sp2-6">EFICIÈNCIA CONSUM:</label>
  	<p>Aquest paràmetre defineix el consum d'energia en cada iteració. Els valors més alts fan que l'espècie necessiti més energia per cicle d'iteració, que significa menys eficiència.</p>
  	<input class="knob" id="amount-sp2-6" name="amount-sp2-6" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[13]?>">
    </p>
    <div id="sp2-6"></div>
    <p>
  	<label for="amount-sp2-7">EFICIÈNCIA RECOLLIDA:</label>
  	<p>D'igual manera que el paràmetre anterior defineix l'eficiència del consum energètic, aquest defineix l'eficiència de la recollida d'energia del manà. Els valors més alts impliquen més eficiència de recollida.</p>
  	<input class="knob" id="amount-sp2-7" name="amount-sp2-7" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[14]?>">
    </p>
    <div id="sp2-7"></div>
    <p>
  	<label for="amount-sp2-8">ENERGIA MÍNIMA PER REPRODUIR-SE:</label>
  	<p>Per permetre la replicació d'espècies, cada individu necessita superar un llindar energètic, la quantitat mínima d'energia necessària per reproduir-se. Els valors més alts signifiquen un llindar superior.</p>
  	<input class="knob" id="amount-sp2-8" name="amount-sp2-8" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[15]?>">
    </p>
    <div id="sp2-8"></div>
  </div>
  <div id="tabs-3">
	<p>
  	<label for="amount-sp3-1">ESPERANÇA DE VIDA:</label>
  	<p>L'esperança de vida és una mesura estadística del temps mitjà que s'espera que visqui un organisme. Una vegada que l'entitat pixèlica es converteix en estable, l'esperança de vida determina quantes iteracions sobreviu.</p>
  	<input class="knob" id="amount-sp3-1" name="amount-sp3-1" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[16]?>">
    </p>
    <div id="sp3-1"></div>
    <p>
  	<label for="amount-sp3-2">INDEX DE REPRODUCCIÓ:</label>
	<p>Quan una entitat píxelica compleix els requisits definits, es poden reproduir a una cel·la adjacent. Aquesta variable determina les possibilitats de reproducció, de manera que un valor superior significa més probabilitats de sobreviure.</p>
  	<input class="knob" id="amount-sp3-2" name="amount-sp3-2" data-width="200" data-min="1" data-max="5000" value="<?=$lifeboxarray[17]?>">
    </p>
    <div id="sp3-2"></div>
    <p>
  	<label for="amount-sp3-3">NAIXAMENT ESPONTANI:</label>
  	<p>La partenogèsia és un tret rar entre espècies que els permet reproduir-se sense aparellar-se. Les espècies dins de LifeBox poden reproduir-se d'una manera similar. En cas que ho aconsegueixin, la descendència es poblarà a l'atzar dins de la graella. Establir aquesta variable amb un valor alt significa grans possibilitats de reproduir-se d'aquesta manera. En cas contrari, si l'usuari decideix reduir aquest valor, la partenogènesi és menys probable.</p>
  	<input class="knob" id="amount-sp3-3" name="amount-sp3-3" data-width="200" data-min="1" data-max="130" value="<?=$lifeboxarray[18]?>">
    </p>
    <div id="sp3-3"></div>
    <p>
  	<label for="amount-sp3-5">GENERACIÓ D'ENERGIA:</label>
  	<p>Cada mana invidivual genera una quantitat d'energia definida per cicle, utilitzada per les altres especies. La generació d'energia baixa significa un entorn deficient per sobreviure.</p>
  	<input class="knob" id="amount-sp3-5" name="amount-sp3-5" data-width="200" data-min="1" data-max="100" value="<?=$lifeboxarray[20]?>">
    </p>
    <div id="sp3-5"></div>
  </div>
</div>
</form>
</div>
 
 
</body>
</html>
