<!DOCTYPE HTML>
<html>

<head>
<?php
$line=0;
$myfile = fopen("temp.log", "r") or die("Unable to open file!");
$datafile=fread($myfile,filesize("temp.log"));
$datafilelines=explode("\n",$datafile);
fclose($myfile);
//while ($line<count($datafilelines)) {
//	$filedata[$line]=explode(",",$datafilelines[$line]);
//	$line++;
//}
//echo $filedata[1][1];
?>
<script type="text/javascript">
window.onload = function () {
	var tchart = new CanvasJS.Chart("temperature",
	{
		animationEnabled: true,
		title:{
			text: "Temperature (ºC)"
		},
		data: [
		{
			type: "spline",
			showInLegend: true,
			color: "#8080FF",
			legendText: "Temperature (ºC)",
			xValueType: "dateTime",		
			dataPoints: [
				<?php
				
				$line=0;
				while ($line<count($datafilelines)-1) {
					$linedata=explode(",",$datafilelines[$line]);
					$data=substr($linedata[0],0,8)."t".substr($linedata[0],-6);
					if ($line<count($datafilelines)-2) {
						echo "{ x: new Date(".(strtotime($data))."*1000), y: ".$linedata[2]."},";
					} else {
						echo "{ x: new Date(".(strtotime($data))."*1000), y: ".$linedata[2]."}";
					}
					$line++;
				}
				?>	
			]
			}
		],
		legend: {
			cursor: "pointer",
			itemclick: function (e) {
				if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
					e.dataSeries.visible = false;
				} else {
					e.dataSeries.visible = true;
			}
			tchart.render();
			}
		}
	});

	var hchart = new CanvasJS.Chart("humidity",
	{
		animationEnabled: true,
		title:{
			text: "Humidity (%)"
		},
		data: [
		{
			type: "spline",
			showInLegend: true,
			color: "#FF8080",
			legendText: "Humidity (%)",			
			dataPoints: [
				<?php
				
				$line=0;
				while ($line<count($datafilelines)-1) {
					$linedata=explode(",",$datafilelines[$line]);
					$data=substr($linedata[0],0,8)."t".substr($linedata[0],-6);
					if ($line<count($datafilelines)-2) {
						echo "{ x: new Date(".(strtotime($data))."*1000), y: ".$linedata[1]."},";
					} else {
						echo "{ x: new Date(".(strtotime($data))."*1000), y: ".$linedata[1]."}";
					}
					$line++;
				}
				?>	
			]
			}
		],
		legend: {
			cursor: "pointer",
			itemclick: function (e) {
				if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
					e.dataSeries.visible = false;
				} else {
					e.dataSeries.visible = true;
			}
			hchart.render();
			}
		}
	});
	
	var lchart = new CanvasJS.Chart("light",
	{
		animationEnabled: true,
		title:{
			text: "Light (0 min - 32 max)"
		},
		data: [
		{
			type: "spline",
			showInLegend: true,
			color: "#80FF80",
			legendText: "Light (0 min - 32 max)",			
			dataPoints: [
				<?php
				
				$line=0;
				while ($line<count($datafilelines)-1) {
					$linedata=explode(",",$datafilelines[$line]);
					$data=substr($linedata[0],0,8)."t".substr($linedata[0],-6);
					if ($line<count($datafilelines)-2) {
						echo "{ x: new Date(".(strtotime($data))."*1000), y: ".$linedata[3]."},";
					} else {
						echo "{ x: new Date(".(strtotime($data))."*1000), y: ".$linedata[3]."}";
					}
					$line++;
				}
				?>	
			]
			}
		],
		legend: {
			cursor: "pointer",
			itemclick: function (e) {
				if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
					e.dataSeries.visible = false;
				} else {
					e.dataSeries.visible = true;
			}
			lchart.render();
			}
		}
	});

	tchart.render();
	hchart.render();
	lchart.render();
}
</script>
<script type="text/javascript" src="canvasjs.min.js"></script>
</head>
<body>
<h1>Real-time data from Weather Station (from <a target="_blank" href="http://projectlog.ferranfabregas.info/how-to-build-a-weather-station-using-raspberry-pi-and-arduino/">ProjectLog</a>)</h1>
<div id="temperature" style="height: 300px; width: 100%;"></div>
<div id="humidity" style="height: 300px; width: 100%;"></div>
<div id="light" style="height: 300px; width: 100%;"></div>
</body>

</html>