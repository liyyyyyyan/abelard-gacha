<?php session_start(); include 'db.php'; 
if ($_POST) {
    $user = $_POST['username'];
    $pass = $_POST['password'];
    $result = $conn->query("SELECT * FROM users WHERE username='$user'");
    if ($row = $result->fetch_assoc()) {
        if (password_verify($pass, $row['password'])) {
            $_SESSION['user'] = $user;
            $_SESSION['id'] = $row['id'];
            header("Location: index.php");
        } else echo "Wrong password!";
    } else echo "User not found!";
}
?>
<!DOCTYPE html><html><body>
<h2>Login</h2>
<form method="post">
Username: <input name="username"><br>
Password: <input type="password" name="password"><br>
<button>Login</button>
</form>
<a href="register.php">Register here</a>
</body></html>