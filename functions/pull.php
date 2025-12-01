<?php
ob_start();
session_start();
header('Content-Type: application/json');

if (!isset($_SESSION['id'])) { echo json_encode(['error'=>'Login required']); exit; }

include 'db.php';
$id    = (int)$_SESSION['id'];
$times = ($_POST['times'] ?? 1) == 10 ? 10 : 1;
$cost  = ($times == 10) ? 2700 : 300;

$user = $conn->query("SELECT gems,pity4,pity5 FROM users WHERE id=$id")->fetch_assoc();
if (!$user || $user['gems'] < $cost) { echo json_encode(['error'=>'Not enough gems']); exit; }

$results = [];
$pity4 = (int)$user['pity4'];
$pity5 = (int)$user['pity5'];

for ($i=0; $i<$times; $i++) {
    $pity4++; $pity5++;
    if ($pity5 >= 50) { $rarity=5; $pity5=0; }
    elseif ($pity4 >= 10) { $rarity=rand(4,5); $pity4=0; }
    else {
        $rate5 = ($pity5>=40)?20+($pity5-40)*6:1;
        $roll = rand(1,100);
        $rarity = ($roll<=$rate5)?5:(($roll<=$rate5+9)?4:3);
        if ($rarity==5) $pity5=0;
        if ($rarity>=4) $pity4=0;
    }
    $char = $conn->query("SELECT name,rarity,img FROM characters WHERE rarity=$rarity ORDER BY RAND() LIMIT 1")->fetch_assoc() ?: ['name'=>'??','rarity'=>3,'img'=>'images/Red.png'];
    $results[] = $char;
}

$newGems = $user['gems'] - $cost;
$conn->query("UPDATE users SET gems=$newGems, pity4=$pity4, pity5=$pity5, pulls=pulls+$times WHERE id=$id");

ob_end_clean();
echo json_encode([
    'gems'    => $newGems,
    'pity4'   => $pity4,
    'pity5'   => $pity5,
    'results' => $results
]);
?>