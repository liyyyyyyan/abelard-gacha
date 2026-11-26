INSERT INTO characters (name, rarity, img)
SELECT seed.character_name, seed.rarity, seed.image_path
FROM (
    SELECT 'Red' AS character_name, 3 AS rarity, 'images/Red.png' AS image_path
    UNION ALL SELECT 'Yellow', 4, 'images/Yellow.png'
    UNION ALL SELECT 'Ultrared', 5, 'images/Ultrared.png'
    UNION ALL SELECT 'Green', 3, 'images/Green.png'
    UNION ALL SELECT 'Black', 3, 'images/Black.png'
    UNION ALL SELECT 'Bodytea', 3, 'images/Bodytea.png'
    UNION ALL SELECT 'Bend', 3, 'images/bend.png'
    UNION ALL SELECT 'Nick', 3, 'images/nick.png'
    UNION ALL SELECT 'Venom', 3, 'images/venom.png'
    UNION ALL SELECT 'Bad Boy', 4, 'images/bad boy.jpg'
    UNION ALL SELECT 'Face Scan', 3, 'images/face scan.png'
    UNION ALL SELECT 'Ble', 3, 'images/ble.jpg'
    UNION ALL SELECT 'Happy', 3, 'images/happy.jpg'
    UNION ALL SELECT '1x1', 4, 'images/1x1.png'
    UNION ALL SELECT 'Forehead', 3, 'images/forehead.png'
    UNION ALL SELECT 'Beggar', 5, 'images/beggar.jpg'
    UNION ALL SELECT 'Cat', 3, 'images/cat.jpg'
    UNION ALL SELECT 'Goth Baddie', 4, 'images/goth baddie.png'
    UNION ALL SELECT 'Lips', 3, 'images/lips.png'
    UNION ALL SELECT 'The Destroyer', 4, 'images/the destroyer.jpg'
    UNION ALL SELECT 'Princess', 4, 'images/princess.png'
    UNION ALL SELECT 'Bai', 4, 'images/bai.jpg'
    UNION ALL SELECT 'Kiss', 3, 'images/kiss.png'
    UNION ALL SELECT 'Cutie', 3, 'images/cutie.webp'
    UNION ALL SELECT 'Von', 3, 'images/von.png'
    UNION ALL SELECT 'Lenlen', 6, 'images/lenlen.png'
    UNION ALL SELECT 'Gray', 3, 'images/gray.png'
    UNION ALL SELECT 'Coco', 3, 'images/coco.png'
    UNION ALL SELECT 'Character 01', 4, 'images/character-01.jpg'
) AS seed
WHERE NOT EXISTS (
    SELECT 1
    FROM characters existing
    WHERE existing.img = seed.image_path
);
