# Referensi Pengantar Pemrograman Game

Referensi berikut dipilih berdasarkan CPMK mata kuliah Pengantar Pemrograman Game. CPMK1 dan CPMK2 menggunakan **Python dengan library Pygame** agar mahasiswa memahami game loop, fisika sederhana, dan algoritma AI secara langsung. Game engine Unity atau Godot mulai digunakan pada CPMK3 dan CPMK4.

## Referensi Utama

1. [Making Games with Python & Pygame — PDF](https://inventwithpython.com/makinggames.pdf)  
   Ebook legal dan gratis karya Al Sweigart. Membahas dasar Pygame melalui proyek permainan, termasuk game loop, event handling, animasi, sprite, collision, dan logika lawan.

2. [Invent Your Own Computer Games with Python — PDF](https://inventwithpython.com/inventwithpython.pdf)  
   Ebook legal dan gratis untuk pengantar pemrograman game dengan Python, dari permainan berbasis teks sampai permainan grafis menggunakan Pygame.

3. [Unity: Introduction to Level Design — PDF](https://assets2.brandfolder.io/bf-boulder-prod/khmctn58vjqkr42wmm3mqvq9/v/1131033155/original/UNITY_Ebook_Introduction%20to%20level%20design%20in%20game%20development%20and%20in%20Unity_V2.pdf)  
   Ebook resmi untuk CPMK3 dan CPMK4 yang membahas prototyping, greyboxing, scene, lighting, aset, scripting, physics, animation, ProBuilder, Polybrush, dan Terrain.

## CPMK1 — Game Loop dan Fisika Sederhana dengan Python/Pygame

- [Pygame Documentation: Quick Start](https://www.pygame.org/docs/)  
  Dokumentasi resmi yang memperlihatkan struktur game loop Pygame, event polling, proses update dan render, pembatasan FPS dengan `pygame.time.Clock`, serta gerakan bebas frame rate menggunakan delta time.

- [Pygame Tutorial: Line-by-Line Chimp](https://www.pygame.org/docs/tut/ChimpLineByLine.html)  
  Tutorial resmi berbasis proyek yang menjelaskan sprite, input, pergerakan, collision, suara, dan struktur loop permainan.

- [Pygame Sprite Documentation](https://www.pygame.org/docs/ref/sprite.html)  
  Referensi resmi untuk `Sprite`, `Group`, `spritecollide`, `groupcollide`, collision berbasis persegi, dan collision berbasis mask.

- [Pygame Mask Documentation](https://www.pygame.org/docs/ref/mask.html)  
  Referensi collision detection per piksel menggunakan bitmask dan integrasinya dengan `pygame.sprite.collide_mask`.

- [Game Loop — Game Programming Patterns](https://gameprogrammingpatterns.com/game-loop.html)  
  Landasan teori mengenai siklus input, update AI/fisika, dan render, termasuk fixed serta variable timestep.

- [Fix Your Timestep! — Gaffer on Games](https://gafferongames.com/post/fix_your_timestep/)  
  Landasan teori untuk fixed timestep, accumulator, stabilitas simulasi, dan gerakan yang tidak bergantung pada frame rate.

- [Numerical Integration — GDC PDF](https://box2d.org/files/ErinCatto_NumericalIntegration_GDC2009.pdf)  
  Materi pendukung untuk menerapkan gerak, kecepatan, percepatan, gravitasi, dan Euler integration di dalam loop Pygame.

Materi praktikum CPMK1 dapat berupa gerak objek dengan `pygame.Vector2`, delta time, gravitasi dan lompatan, pantulan, serta collision menggunakan `pygame.Rect` atau mask.

## CPMK2 — AI Dasar untuk NPC dengan Python/Pygame

- [Game AI: Pathfinding — PDF](https://edirlei.com/aulas/game-ai-2020/GAME_AI_Lecture_02_Pathfinding_2020.pdf)  
  Dasar akademik BFS, DFS, Dijkstra, A*, heuristic, waypoint graph, dan pencarian jalur optimal. Algoritmanya dapat diimplementasikan menggunakan struktur data Python.

- [Game AI: Finite State Machines — PDF](https://edirlei.com/aulas/game-ai-2020/GAME_AI_Lecture_03_Finite_State_Machines_2020.pdf)  
  Dasar FSM untuk perilaku NPC seperti idle, patrol, chase, attack, dan flee. Konsep state dan transition dapat diterapkan sebagai class atau fungsi Python.

- [Writing a Game in Python with Pygame, Part III: Pathfinding](https://eli.thegreenplace.net/2009/01/09/writing-a-game-in-python-with-pygame-part-iii)  
  Implementasi dan visualisasi algoritma A* pada grid menggunakan Python dan Pygame, dilengkapi kode contoh.

- [How to Create a Video Game AI with Python](https://reintech.io/blog/how-to-create-a-video-game-ai-with-python)  
  Tutorial Python/Pygame mengenai persepsi NPC, FSM, patrol dan chase, serta pathfinding A* berbasis grid.

- [Making Games with Python & Pygame — PDF](https://inventwithpython.com/makinggames.pdf)  
  Contoh permainan lengkap yang dapat dipakai untuk mengidentifikasi dan memodifikasi logika musuh sederhana.

Materi praktikum CPMK2 dapat dimulai dari NPC yang mengejar pemain menggunakan vektor, dilanjutkan FSM `idle-patrol-chase`, lalu A* menggunakan `heapq` pada peta berbasis grid yang divisualisasikan dengan Pygame.

## CPMK3 — Menggunakan Game Engine untuk Membangun Level

- [Unity Learn](https://learn.unity.com/)  
  Kursus resmi gratis dengan jalur Unity Essentials, Junior Programmer, dan Game Development.

- [Unity Junior Programmer: Create with Code](https://learn.unity.com/mission/programming-simple-functionality?pathwayId=5f7e17e1edbc2a5ec21a20af)  
  Proyek praktis mengenai scripting, physics, gameplay mechanics, sound, effects, dan UI.

- [Godot Official Documentation](https://docs.godotengine.org/en/stable/)  
  Dokumentasi dan tutorial resmi yang juga tersedia dalam format HTML offline dan EPUB.

- [Godot: Your First 2D Game](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html)  
  Tutorial mengenai scene, node, scripting, player, enemy, collision, animation, HUD, dan game lifecycle.

## CPMK4 — Mengintegrasikan Aset Audio dan Visual

- [Unity Asset Importing](https://docs.unity3d.com/Manual/ImportingAssets.html)  
  Menjelaskan pipeline impor gambar, model, animasi, audio, dan konfigurasi aset melalui Inspector.

- [Godot Asset Import Process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)  
  Menjelaskan pipeline aset Godot untuk gambar, scene, model, font, dan audio.

- [Godot: Importing Audio Samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html)  
  Menjelaskan WAV, Ogg, MP3, looping, compression, serta penggunaan `AudioStreamPlayer`, `AudioStreamPlayer2D`, dan `AudioStreamPlayer3D`.

## Rekomendasi Penggunaan

- Gunakan **Python 3 dan Pygame** untuk seluruh praktikum CPMK1 dan CPMK2.
- Gunakan **Making Games with Python & Pygame** sebagai buku praktikum utama.
- Gunakan dokumentasi resmi Pygame sebagai acuan API game loop, waktu, vektor, sprite, dan collision.
- Gunakan slide **Game AI: Pathfinding** dan **Finite State Machines** sebagai teori, kemudian implementasikan algoritmanya sendiri dengan Python/Pygame tanpa `NavMesh` dari game engine.
- Mulai gunakan **Unity atau Godot** pada CPMK3 untuk membangun level dan lanjutkan pada CPMK4 untuk integrasi aset.
- Gunakan dokumentasi resmi Unity atau Godot sebagai acuan teknis terbaru untuk CPMK3 dan CPMK4.
