<?php
echo "PHP is working!<br>";

include 'db.php';
echo "Database connected!<br>";

session_start();
echo "Session ID: " . session_id() . "<br>";
echo "User ID: " . ($_SESSION['id'] ?? 'not set') . "<br>";

$result = $conn->query("SELECT * FROM characters LIMIT 1");
if ($result) {
    echo "Characters table OK! Found " . $result->num_rows . " row(s)<br>";
    $row = $result->fetch_assoc();
    print_r($row);
} else {
    echo "ERROR: " . $conn->error;
}
?>