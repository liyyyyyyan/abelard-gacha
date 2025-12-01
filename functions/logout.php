<?php
session_start();
session_unset();
session_destroy();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Logged Out</title>
    <style>
        body { 
            background: #1a0033; 
            color: white; 
            font-family: Arial; 
            text-align: center; 
            padding-top: 100px; 
        }
        a {
            padding: 15px 30px;
            background: #ff3399;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 20px;
        }
        a:hover { background: #ff66bb; }
    </style>
</head>
<body>
    <h1>Successfully logged out!</h1>
    <p>See you next time, whale!</p>
    <br><br>
    <a href="login.php">Login Again</a>
</body>
</html>