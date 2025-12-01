<?php 
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}

include 'db.php';
$user = $_SESSION['user'];

// SAFE QUERY — WALANG SQL INJECTION
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
$stmt->bind_param("s", $user);
$stmt->execute();
$data = $stmt->get_result()->fetch_assoc();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ABELARD GACHA</title>
    <link rel="stylesheet" href="abelardsstype.css">
</head>
<body>
    <h1>Welcome, <?=htmlspecialchars($user)?>!</h1>
    <div class="gems">Gems: <span id="gems"><?=$data['gems']?></span></div>
    <div style="margin:20px; font-size:20px; color:gold;">
        4★ Pity: <span id="pity4"><?=$data['pity4']?></span>/10<br>
        5★ Pity: <span id="pity5"><?=$data['pity5']?></span>/50
    </div>

    <button onclick="singlePull()">Single Pull (300)</button>
    <button onclick="tenPull()">10x Pull (2700)</button>

    <div id="result" style="margin:40px; min-height:200px;"></div>

    <br><br>
    <a href="logout.php" style="color:cyan; font-size:18px;">[ Logout ]</a>

    <script>
    function pull(times) {
        fetch('pull.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'times=' + times
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            document.getElementById("gems").textContent = data.gems;
            document.getElementById("pity4").textContent = data.pity4;
            document.getElementById("pity5").textContent = data.pity5;
            document.getElementById("result").innerHTML = "";

            data.results.forEach((char, i) => {
                setTimeout(() => {
                    const card = document.createElement("div");
                    card.className = `card r${char.rarity} ${char.rarity==5?'sparkle':''}`;
                    card.innerHTML = `<img src="${char.img}"><h3>${char.rarity}★ ${char.name}</h3>`;
                    document.getElementById("result").appendChild(card);
                }, i * 350);
            });
        })
        .catch(err => alert("Pull error — pero try mo ulit, malapit na talaga!"));
    }
    function singlePull() { pull(1); }
    function tenPull()   { pull(10); }
    </script>
</body>
</html>