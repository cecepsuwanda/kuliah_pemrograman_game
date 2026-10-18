"""Mesin keadaan pada NPC: berdiam, berpatroli, mengejar, dan menyerang.

NPC pada program ini memiliki empat keadaan. Setiap keadaan memiliki perilaku
sendiri, sedangkan perpindahannya diatur oleh syarat berupa jarak terhadap
pemain dan oleh pewaktu (timer).

Perpindahan yang sah:
    berdiam    -> berpatroli : setelah berdiam 1,5 detik
    berdiam    -> mengejar   : pemain masuk jari-jari persepsi
    berpatroli -> mengejar   : pemain masuk jari-jari persepsi
    berpatroli -> berdiam    : satu putaran patroli selesai
    mengejar   -> menyerang  : pemain masuk jangkauan serang
    mengejar   -> berdiam    : pemain tidak terlihat selama 1 detik
    menyerang  -> mengejar   : pemain keluar dari jangkauan serang

Program mencatat setiap perpindahan keadaan, lalu memeriksa bahwa seluruh
perpindahan yang terjadi termasuk perpindahan yang sah.

Pengendalian:
    W A S D atau tombol panah : menggerakkan pemain
    ESC                       : mengakhiri program

Pemakaian:
    python ch09_fsm.py
    python ch09_fsm.py --frames 900 --scenario     (uji perpindahan keadaan)
    python ch09_fsm.py --frames 400 --auto-run     (pemain bergerak melingkar)
"""

from __future__ import annotations

import argparse
import math
import sys

import pygame

BACKGROUND_COLOR = (24, 32, 52)
PLAYER_COLOR = (46, 117, 182)
TEXT_COLOR = (255, 255, 255)
HINT_COLOR = (150, 165, 190)
RADIUS_COLOR = (80, 100, 140)
ATTACK_COLOR = (150, 90, 80)
WAYPOINT_COLOR = (110, 130, 165)

IDLE_STATE = "berdiam"
PATROL_STATE = "berpatroli"
CHASE_STATE = "mengejar"
ATTACK_STATE = "menyerang"

STATE_COLORS = {
    IDLE_STATE: (120, 120, 130),
    PATROL_STATE: (70, 150, 110),
    CHASE_STATE: (190, 74, 66),
    ATTACK_STATE: (222, 130, 50),
}

# Perpindahan yang sah. Dipakai untuk memeriksa catatan perpindahan keadaan.
LEGAL_TRANSITIONS = {
    IDLE_STATE: {PATROL_STATE, CHASE_STATE},
    PATROL_STATE: {IDLE_STATE, CHASE_STATE},
    CHASE_STATE: {ATTACK_STATE, IDLE_STATE},
    ATTACK_STATE: {CHASE_STATE},
}

WINDOW_WIDTH = 880
WINDOW_HEIGHT = 600
PLAYER_SPEED = 250.0
PLAYER_SIZE = 30
NPC_SIZE = 28

DEFAULT_RADIUS = 260.0
DEFAULT_ATTACK_RANGE = 46.0
DEFAULT_SPEED = 150.0
PATROL_SPEED = 90.0
IDLE_SECONDS = 1.5
GIVE_UP_SECONDS = 1.0
ATTACK_COOLDOWN = 0.8
WAYPOINT_REACHED = 12.0
DEFAULT_FPS = 60

# Jalur patroli di sudut kiri bawah, jauh dari sudut kanan atas tempat pemain
# berdiri pada skenario pengujian.
WAYPOINTS = ((150, 380), (330, 380), (330, 540), (150, 540))


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Mesin keadaan pada NPC")
    parser.add_argument("--radius", type=float, default=DEFAULT_RADIUS,
                        help="jari-jari persepsi, dalam piksel")
    parser.add_argument("--attack-range", type=float, default=DEFAULT_ATTACK_RANGE,
                        help="jangkauan serang, dalam piksel")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED,
                        help="kecepatan mengejar, dalam piksel per detik")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--scenario", action="store_true",
                        help="jalankan skenario pengujian perpindahan keadaan")
    parser.add_argument("--auto-run", action="store_true",
                        help="gerakkan pemain secara otomatis")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


class Player(pygame.sprite.Sprite):
    """Pemain yang digerakkan tombol."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, delta_seconds: float, direction) -> None:
        """Memperbarui gerak pemain."""
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * PLAYER_SPEED
        else:
            self.velocity = pygame.Vector2(0, 0)

        self.position += self.velocity * delta_seconds
        half = PLAYER_SIZE / 2
        self.position.x = max(half, min(WINDOW_WIDTH - half, self.position.x))
        self.position.y = max(half, min(WINDOW_HEIGHT - half, self.position.y))
        self.rect.center = (round(self.position.x), round(self.position.y))


class Npc(pygame.sprite.Sprite):
    """NPC dengan mesin keadaan empat keadaan."""

    def __init__(self, x: float, y: float, radius: float, attack_range: float,
                 speed: float) -> None:
        super().__init__()
        self.image = pygame.Surface((NPC_SIZE, NPC_SIZE))
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.attack_range = attack_range
        self.speed = speed

        # Keadaan mesin keadaan.
        self.state = IDLE_STATE
        self.distance = 0.0
        self.idle_timer = 0.0
        self.lost_timer = 0.0
        self.attack_timer = 0.0
        self.attacks = 0
        self.waypoint_index = 0
        self.waypoints_visited = 0
        self.frames = 0
        self.transitions: list[tuple[int, str]] = [(0, self.state)]

    # ---------- Keputusan: keadaan berikutnya ----------
    def decide(self, delta_seconds: float) -> str:
        """Menentukan keadaan berikutnya menurut jarak dan pewaktu."""
        self.attack_timer = max(0.0, self.attack_timer - delta_seconds)

        if self.state == IDLE_STATE:
            self.idle_timer += delta_seconds
            if self.distance <= self.radius:
                return CHASE_STATE
            if self.idle_timer >= IDLE_SECONDS:
                return PATROL_STATE
            return IDLE_STATE

        if self.state == PATROL_STATE:
            if self.distance <= self.radius:
                return CHASE_STATE
            if self.waypoints_visited >= len(WAYPOINTS):
                return IDLE_STATE
            return PATROL_STATE

        if self.state == CHASE_STATE:
            if self.distance <= self.attack_range:
                return ATTACK_STATE
            if self.distance <= self.radius:
                return CHASE_STATE
            self.lost_timer += delta_seconds
            if self.lost_timer >= GIVE_UP_SECONDS:
                return IDLE_STATE
            return CHASE_STATE

        if self.state == ATTACK_STATE:
            if self.distance > self.attack_range * 1.2:
                return CHASE_STATE
            return ATTACK_STATE

        return IDLE_STATE

    # ---------- Tindakan: perilaku keadaan yang aktif ----------
    def act(self, delta_seconds: float, player: Player) -> None:
        """Menjalankan perilaku keadaan yang sedang aktif."""
        if self.state == IDLE_STATE:
            self.velocity = pygame.Vector2(0, 0)

        elif self.state == PATROL_STATE:
            target = pygame.Vector2(*WAYPOINTS[self.waypoint_index])
            to_target = target - self.position
            if to_target.length() <= WAYPOINT_REACHED:
                # Sampai di sebuah titik patroli: lanjut ke titik berikutnya.
                self.waypoint_index = (self.waypoint_index + 1) % len(WAYPOINTS)
                self.waypoints_visited += 1
                to_target = pygame.Vector2(*WAYPOINTS[self.waypoint_index]) \
                    - self.position
            if to_target.length_squared() > 0:
                self.velocity = to_target.normalize() * PATROL_SPEED
            else:
                self.velocity = pygame.Vector2(0, 0)

        elif self.state == CHASE_STATE:
            to_player = player.position - self.position
            if to_player.length_squared() > 0:
                self.velocity = to_player.normalize() * self.speed
            else:
                self.velocity = pygame.Vector2(0, 0)

        elif self.state == ATTACK_STATE:
            self.velocity = pygame.Vector2(0, 0)
            if self.attack_timer <= 0.0:
                self.attacks += 1
                self.attack_timer = ATTACK_COOLDOWN

        self.position += self.velocity * delta_seconds
        half = NPC_SIZE / 2
        self.position.x = max(half, min(WINDOW_WIDTH - half, self.position.x))
        self.position.y = max(half, min(WINDOW_HEIGHT - half, self.position.y))
        self.rect.center = (round(self.position.x), round(self.position.y))

    # ---------- Pembaruan ----------
    def enter_state(self, state: str) -> None:
        """Menyiapkan keadaan yang baru dimasuki."""
        self.state = state
        if state == IDLE_STATE:
            self.idle_timer = 0.0
        elif state == PATROL_STATE:
            self.waypoints_visited = 0
        elif state == CHASE_STATE:
            self.lost_timer = 0.0
        if not self.transitions or self.transitions[-1][1] != state:
            self.transitions.append((self.frames, state))

    def update(self, delta_seconds: float, player: Player) -> None:
        """Menjalankan satu putaran mesin keadaan."""
        to_player = player.position - self.position
        self.distance = to_player.length()
        self.frames += 1

        next_state = self.decide(delta_seconds)
        if next_state != self.state:
            self.enter_state(next_state)

        self.act(delta_seconds, player)
        self.image.fill(STATE_COLORS[self.state])


def auto_player_position(frames: int, fps: int) -> pygame.Vector2:
    """Posisi pemain pada jalur melingkar, untuk pengujian."""
    sudut = frames / fps * 1.1
    return pygame.Vector2(WINDOW_WIDTH / 2 + 290 * math.cos(sudut),
                          WINDOW_HEIGHT / 2 + 200 * math.sin(sudut))


def scenario_player_position(frames: int) -> pygame.Vector2:
    """Posisi pemain pada jalur tetap yang memicu seluruh perpindahan keadaan.

    Pemain berdiri di sudut kanan bawah, yaitu sudut yang paling jauh dari
    jalur patroli NPC di sudut kiri bawah. Jarak terjauh itu diperlukan agar
    NPC benar-benar kehilangan pemain ketika pemain menghilang, walaupun NPC
    masih bergerak mengejar selama pewaktu tenggang berjalan.
    """
    if frames < 150:
        return pygame.Vector2(860, 570)     # jauh: di luar jari-jari persepsi
    if frames < 420:
        return pygame.Vector2(520, 200)     # di dalam jangkauan persepsi
    return pygame.Vector2(860, 570)         # jauh kembali, sehingga NPC menyerah


# Urutan keadaan yang diharapkan pada skenario pengujian.
EXPECTED_SEQUENCE = [
    IDLE_STATE, PATROL_STATE, CHASE_STATE, ATTACK_STATE,
    CHASE_STATE, IDLE_STATE, PATROL_STATE,
]


def check_transitions(transitions: list[tuple[int, str]],
                      periksa_kelengkapan: bool = False) -> list[str]:
    """Memeriksa catatan perpindahan keadaan dan mengembalikan daftar temuan.

    Keabsahan setiap perpindahan diperiksa selalu, sebab hal itu berlaku pada
    segala keadaan permainan. Kelengkapan seluruh keadaan hanya diperiksa pada
    skenario pengujian, sebab pada permainan biasa ada keadaan yang memang
    belum sempat terjadi.
    """
    masalah: list[str] = []
    urutan = [keadaan for _, keadaan in transitions]

    for sebelumnya, berikutnya in zip(urutan, urutan[1:]):
        if berikutnya not in LEGAL_TRANSITIONS.get(sebelumnya, set()):
            masalah.append(
                f"perpindahan tidak sah: {sebelumnya} -> {berikutnya}")

    if periksa_kelengkapan:
        for wajib in (IDLE_STATE, PATROL_STATE, CHASE_STATE, ATTACK_STATE):
            if wajib not in urutan:
                masalah.append(f"keadaan {wajib} tidak pernah terjadi")

        if urutan and urutan[0] != IDLE_STATE:
            masalah.append("keadaan awal bukan berdiam")

    return masalah


def main() -> int:
    args = parse_arguments()

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Bab IX - mesin keadaan pada NPC")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    player = Player(830, 60)
    npc = Npc(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, args.radius,
              args.attack_range, args.speed)
    npcs = pygame.sprite.Group(npc)

    frames = 0
    delta_seconds = 0.0
    running = True

    if args.auto_close and not args.frames:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while running:
        # ---------- Tahap 1: membaca masukan ----------
        direction = pygame.Vector2(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        if args.scenario:
            player.position = scenario_player_position(frames)
            player.rect.center = (round(player.position.x),
                                  round(player.position.y))
        elif args.auto_run:
            player.position = auto_player_position(frames, args.fps)
            player.rect.center = (round(player.position.x),
                                  round(player.position.y))
        else:
            player.update(delta_seconds, direction)

        # ---------- Tahap 2: memperbarui keadaan ----------
        npc.update(delta_seconds, player)
        frames += 1
        measured_fps = clock.get_fps()

        # ---------- Tahap 3: menayangkan ----------
        screen.fill(BACKGROUND_COLOR)

        pygame.draw.circle(screen, RADIUS_COLOR, npc.rect.center,
                           int(npc.radius), 1)
        pygame.draw.circle(screen, ATTACK_COLOR, npc.rect.center,
                           int(npc.attack_range), 1)

        for nomor, titik in enumerate(WAYPOINTS):
            pygame.draw.circle(screen, WAYPOINT_COLOR, titik, 4, 1)
            pygame.draw.line(screen, WAYPOINT_COLOR, titik,
                             WAYPOINTS[(nomor + 1) % len(WAYPOINTS)], 1)

        pygame.draw.line(screen, (90, 110, 150), npc.rect.center,
                         player.rect.center, 1)
        npcs.draw(screen)
        screen.blit(player.image, player.rect)

        info = [
            f"Bingkai     : {frames:5d}",
            f"Laju bingkai: {measured_fps:6.1f} FPS",
            f"Keadaan     : {npc.state}",
            f"Jarak       : {npc.distance:6.1f} piksel",
            f"Pewaktu     : diam {npc.idle_timer:4.1f}   "
            f"hilang {npc.lost_timer:4.1f}   serang {npc.attack_timer:4.1f}",
            f"Serangan    : {npc.attacks}",
        ]
        y = 16
        for line in info:
            screen.blit(font.render(line, True, TEXT_COLOR), (16, y))
            y += 21

        urutan = " -> ".join(keadaan for _, keadaan in npc.transitions)
        screen.blit(font.render(f"Urutan keadaan: {urutan}", True, TEXT_COLOR),
                    (16, WINDOW_HEIGHT - 46))
        hint = font.render("WASD atau panah: gerakkan pemain   ESC: keluar",
                            True, HINT_COLOR)
        screen.blit(hint, (16, WINDOW_HEIGHT - 26))
        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        delta_seconds = clock.tick(args.fps) / 1000.0

        if args.frames and frames >= args.frames:
            running = False

    pygame.quit()

    print(f"Bingkai dijalankan : {frames}")
    print(f"Serangan dilakukan : {npc.attacks}")
    print("Catatan perpindahan keadaan (bingkai, keadaan):")
    for bingkai, keadaan in npc.transitions:
        print(f"    {bingkai:5d}  {keadaan}")

    masalah = check_transitions(npc.transitions, args.scenario)
    if masalah:
        for satu in masalah:
            print(f"  ! {satu}")
        print("Hasil pemeriksaan  : ADA TEMUAN")
    else:
        print("Hasil pemeriksaan  : seluruh perpindahan sah")

    if args.scenario:
        urutan = [keadaan for _, keadaan in npc.transitions]
        if urutan == EXPECTED_SEQUENCE:
            print("Hasil skenario     : SESUAI dengan urutan yang diharapkan")
        else:
            print("Hasil skenario     : TIDAK SESUAI")
            print(f"    diharapkan: {' -> '.join(EXPECTED_SEQUENCE)}")
            print(f"    terjadi   : {' -> '.join(urutan)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
