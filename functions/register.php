<?php include 'db.php';
if ($_POST) {
    $user = trim($_POST['username']);
 $pass = password_hash($_POST['password'], PASSWORD_DEFAULT);

 // Check if username already exists
 $check = $conn->prepare("SELECT id FROM users WHERE username = ?");
 $check->bind_param("s", $user);
 $check->execute();
 if ($check->get_result()->num_rows > 0) {
     echo "<b style='color:red'>Username already taken!</b><br><br>";
 } else {
     $stmt = $conn->prepare("INSERT INTO users (username, password, gems) VALUES (?, ?, 10000)");
     $stmt->bind_param($stmt, "s", $user, $pass);
     $stmt->execute();
     echo "<b style='color:cyan'>Registered na! Gems: 10,000<br><a href='login.php'>Login na</a></b>";
     exit;
 }
}
?>
<!DOCTYPE html><html><head><meta charset="utf-8"><title>Register • Abelard Gacha</title>
<style>body{background:#1a0033;color:white;font-family:Arial;text-align:center;padding:100px;}
input,button{padding:12px;margin:10px;width:250px;border-radius:50px;border:none;font-size:18px}</style></head><body>
<h1 style="color:gold">ABELARD GACHA</h1><h2>Register</h2>
<form method="post">
<input name="username" placeholder="Username" required><br>
<input name="password" type="password" placeholder="Password" required><br>
<button type="submit">Create Account (10k gems free!)</button>
</form><br>
<a href="login.php" style="color:cyan">Already have account? Login here</a>
</body></html>