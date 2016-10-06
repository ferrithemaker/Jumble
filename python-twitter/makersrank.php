<html>
<head>
<title>Top 1k makers on Twitter</title>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">
<script type="text/javascript" language="javascript" src="//code.jquery.com/jquery-1.12.3.js">
</script>
<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js">
</script>
</head>
<body>
<?php
$username = "";
$password = "";
$hostname = ""; 

//connection to the database
$conn = new mysqli($servername, $username, $password,'twittertrends');

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$query = "SELECT * FROM capture WHERE points>1 order by points ASC limit 1000";

$result = mysqli_query($conn, $query);

?>
<h2>Real-time top 1k makers on Twitter</h2>
<table id="makertrendstable" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
		<th></th>
                <th>Name</th>
                <th>User</th>
                <th>Location</th>
                <th>Impacts</th>
		<th>Last impact</th>
		<th>Followers</th>
		<th>Friends</th>
                <th>TFF ratio</th>
                <th>Overall (*beta)</th>
		<th>Description</th>
            </tr>
        </thead>
        <tbody>
	<?php
	foreach ($result as $row) {
		$color="black";
		if ($row['followers']==0) { $row['followers']=1; $color="red"; }
		if ($row['friends']==0) { $row['friends']=1; $color="blue"; }
		echo "<tr style=\"color:".$color."\">";
		echo "<td><img src=\"".$row['photo']."\"></td>";
		echo "<td>".$row['nickname']."</td>";
		echo "<td><a href=\"https://twitter.com/".$row['user']."\" target=\"_blank\">@".$row['user']."</td>";
		echo "<td>".$row['geoLocation']."</td>";
		echo "<td>".$row['points']."</td>";
		echo "<td>".$row['date']."</td>";
		echo "<td>".$row['followers']."</td>";
		echo "<td>".$row['friends']."</td>";
		echo "<td>".($row['followers']/$row['friends'])."</td>";
		echo "<td>".((($row['followers']/$row['friends'])*$row['points'])*($row['followers']/1000))."</td>";
		echo "<td>".$row['description']."</td>";
		echo "</tr>";
	}
	?>
    </table>
</body>
</html>
<script>
$('#makertrendstable').dataTable( {
  "order": [[ 9, "desc" ]],
  "pageLength": 25,
  "aoColumns": [
        { "bSortable": false }, // <-- disable sorting for column 3
        null,
	null,
	null,
	null,
	null,
	null,
	null,
	null,
	null,
	null
     ]
} );
</script>
