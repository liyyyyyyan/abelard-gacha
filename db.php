PHP<?php
$conn = new mysqli("localhost", "root", "", "gacha_abelard");
if ($conn->connect_error) die("Connection failed");
?>