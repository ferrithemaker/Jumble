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
  <title>Lifebox Manager</title>
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
						  '&amount-sp2-1='+$("#amount-sp2-1").val()+
						  '&amount-sp2-2='+$("#amount-sp2-2").val()+
						  '&amount-sp2-3='+$("#amount-sp2-3").val()+
						  '&amount-sp2-4='+$("#amount-sp2-4").val()+
						  '&amount-sp3-1='+$("#amount-sp3-1").val()+
						  '&amount-sp3-2='+$("#amount-sp3-2").val()+
						  '&amount-sp3-3='+$("#amount-sp3-3").val()
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
    <li style="background: lightblue;"><a href="#tabs-1">Yellow</a></li>
    <li style="background: lightblue;"><a href="#tabs-2">Blue</a></li>
    <li style="background: lightblue;"><a href="#tabs-3">Green (food)</a></li>
  </ul>
  <div id="tabs-1">
    <p>
  	<label for="amount-sp1-1">LIFE:</label>
  	<p>Life expectancy of yellow species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp1-1" name="amount-sp1-1" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[4]?>">
    </p>
    <div id="sp1-1"></div>
    <p>
  	<label for="amount-sp1-2">REPRODUCTION:</label>
  	<p>Reproduction capability of yellow species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp1-2" name="amount-sp1-2" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[3]?>">
    </p>
    <div id="sp1-2"></div>
    <p>
  	<label for="amount-sp1-3">EFFICIENCY:</label>
  	<p>Energy consumption of yellow species individuals. Low values are better.</p>
	<input class="knob" id="amount-sp1-3" name="amount-sp1-3" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[5]?>">
    </p>
    <div id="sp1-3"></div>
    <p>
  	<label for="amount-sp1-4">GATHERING:</label>
  	<p>Energy gathering of yellow species individuals from green species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp1-4" name="amount-sp1-4" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[6]?>">
    </p>
  </div>
  <div id="tabs-2">
	<p>
  	<label for="amount-sp2-1">LIFE:</label>
  	<p>Life expectancy of blue species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp2-1" name="amount-sp2-1" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[7]?>">
    </p>
    <div id="sp2-1"></div>
    <p>
  	<label for="amount-sp2-2">REPRODUCTION:</label>
	<p>Reproduction capability of blue species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp2-2" name="amount-sp2-2" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[8]?>">
    </p>
    <div id="sp2-2"></div>
    <p>
  	<label for="amount-sp2-3">EFFICIENCY:</label>
  	<p>Energy consumption of blue species individuals. Low values are better.</p>
  	<input class="knob" id="amount-sp2-3" name="amount-sp2-3" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[9]?>">
    </p>
    <div id="sp2-3"></div>
    <p>
  	<label for="amount-sp2-4">GATHERING:</label>
  	<p>Energy gathering of blue species individuals from green species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp2-4" name="amount-sp2-4" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[10]?>">
    </p>
  </div>
  <div id="tabs-3">
	<p>
  	<label for="amount-sp3-1">LIFE:</label>
  	<p>Life expectancy of green species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp3-1" name="amount-sp3-1" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[0]?>">
    </p>
    <div id="sp3-1"></div>
    <p>
  	<label for="amount-sp3-2">REPRODUCTION:</label>
	<p>Reproduction capability of green species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp3-2" name="amount-sp3-2" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[1]?>">
    </p>
    <div id="sp3-2"></div>
    <p>
  	<label for="amount-sp3-3">GENERATION:</label>
  	<p>Energy generation of green species individuals. High values are better.</p>
  	<input class="knob" id="amount-sp3-3" name="amount-sp3-3" data-width="200" data-min="1" data-max="1023" value="<?=$lifeboxarray[2]?>">
    </p>
  </div>
</div>
</form>
</div>
 
 
</body>
</html>
