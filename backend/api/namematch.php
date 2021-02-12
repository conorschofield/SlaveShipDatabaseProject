<?php
/**
 * Returns the list of policies.
 */
require 'database.php';

$policies = [];
$sql = "SELECT Uniq, CaseN FROM Cases";

if($result = mysqli_query($con,$sql))
{
  $i = 0;
  while($row = mysqli_fetch_assoc($result))
  {
    $policies[$i]['Uniq']    = $row['Uniq'];
    $policies[$i]['CaseN'] = $row['CaseN'];
    $i++;
  }

  echo json_encode($policies);
}
else
{
  http_response_code(404);
}