"""Inti permainan: siklus, kedua level, dan peralihan antarlevel."""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Guard, Player, cell_center
from .fsm import CHASE, GuardBrain
from .levels import ARTEFACT_LAYOUT, build_lorong, build_rak
from .pathfinding import find_path


class Game:
    """Menjalankan satu permainan yang terdiri atas dua level berurutan."""

    def __init__(self, args) -> None:
        pygame.init()
        self.args = args
        self.screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(f"{S.TITLE} | {args.fps} FPS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.small = pygame.font.Font(None, 22)
        self.frames = 0
        self.running = True
        self.reset()

    # --- penyiapan ----------------------------------------------------
    def start_level(self, level: int) -> None:
        """Memulai permainan langsung pada level yang diminta."""
        if level == 2:
            self._load_lorong()

    def reset(self) -> None:
        self.score = 0
        self.lives = S.START_LIVES
        self.mode = "rak"
        self.message = ""
        self.guard = None
        self.brain = None
        self.path: list[tuple[int, int]] = []
        self.repath_timer = 0.0
        self.artefacts_left = len(ARTEFACT_LAYOUT)
        self._load_rak()

    def _load_rak(self) -> None:
        self.rak = build_rak()
        self.player = Player(*self.rak["spawn"])
        self.solids = self.rak["solids"]
        self.rak["door"].set_open(False)

    def _load_lorong(self) -> None:
        self.mode = "lorong"
        self.lorong = build_lorong(self.args.scenario)
        start = self.lorong["start"]
        pos = cell_center(start)
        self.player = Player(pos.x - S.PLAYER_SIZE / 2,
                             pos.y - S.PLAYER_SIZE / 2)
        self.guard = Guard(self.lorong["guard_start"])
        self.brain = GuardBrain(self.lorong["waypoints"])
        self.path = []
        self.repath_timer = 0.0

    # --- siklus -------------------------------------------------------
    def run(self) -> int:
        while self.running:
            delta_seconds = self.clock.tick(self.args.fps) / 1000.0
            self.handle_events()
            self.update(delta_seconds)
            self.draw()
            pygame.display.flip()
            self.frames += 1
            if self.frames % 30 == 0:
                pygame.display.set_caption(
                    f"{S.TITLE} | {int(self.clock.get_fps())} FPS")
            if self.args.frames and self.frames >= self.args.frames:
                self.running = False
            if self.args.auto_close and self.frames >= 2:
                break
        pygame.quit()
        return 0

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.mode == "rak":
                    self.player.jump()
                elif event.key == pygame.K_r and self.mode in ("kalah", "menang"):
                    self.reset()

    def update(self, delta_seconds: float) -> None:
        if self.mode == "rak":
            self._update_rak(delta_seconds)
        elif self.mode == "lorong":
            self._update_lorong(delta_seconds)
        self.player.respawn_timer = max(0.0, self.player.respawn_timer
                                       - delta_seconds)

    # --- level Rak ----------------------------------------------------
    def _update_rak(self, delta_seconds: float) -> None:
        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) \
            - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player.update_side(delta_seconds, direction, self.solids)

        door = self.rak["door"]
        collected = pygame.sprite.spritecollide(self.player,
                                                self.rak["artefacts"], True)
        for _ in collected:
            self.score += S.ARTEFACT_POINTS
            self.artefacts_left -= 1
        door.set_open(self.artefacts_left == 0)

        if self.player.respawn_timer <= 0.0:
            hit = pygame.sprite.spritecollide(self.player, self.rak["crates"],
                                              False)
            if hit:
                self._lose_life(self.rak["spawn"])

        if door.open and self.player.rect.colliderect(door.rect):
            self._load_lorong()

    # --- level Lorong -------------------------------------------------
    def _update_lorong(self, delta_seconds: float) -> None:
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            int(keys[pygame.K_RIGHT] or keys[pygame.K_d])
            - int(keys[pygame.K_LEFT] or keys[pygame.K_a]),
            int(keys[pygame.K_DOWN] or keys[pygame.K_s])
            - int(keys[pygame.K_UP] or keys[pygame.K_w]))
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.player.update_top_down(delta_seconds, direction,
                                    self.lorong["wall_rects"])

        state = self.brain.update(delta_seconds, self.guard.position,
                                  self.player.position)
        self.guard.set_state(state)
        if state == CHASE:
            self._chase(delta_seconds)
        else:
            self._patrol(delta_seconds)

        if self.player.respawn_timer <= 0.0:
            jarak = (pygame.Vector2(self.player.rect.center)
                     - self.guard.position).length()
            if jarak < (S.PLAYER_SIZE + S.GUARD_SIZE) / 2:
                self._caught()

        exit_pos = cell_center(self.lorong["exit"])
        if (self.player.position - exit_pos).length() < S.CELL * 0.6:
            self.mode = "menang"
            self.message = "Semua artefak sampai di pintu keluar."

    def _patrol(self, delta_seconds: float) -> None:
        target = self.brain.patrol_point()
        if self.guard.walk_to(target, delta_seconds, S.GUARD_PATROL_SPEED):
            self.brain.next_patrol_point()

    def _chase(self, delta_seconds: float) -> None:
        """Saat mengejar, rute dihitung ulang secara berkala dengan A*."""
        self.repath_timer -= delta_seconds
        player_cell = (int((self.player.position.x - S.GRID_OFFSET_X)
                           // S.CELL),
                       int((self.player.position.y - S.GRID_OFFSET_Y)
                           // S.CELL))
        if self.repath_timer <= 0.0 or not self.path:
            self.path = find_path(self.lorong["rows"], self.guard.cell(),
                                  player_cell)
            self.guard.path = self.path
            self.guard.path_index = 0
            self.repath_timer = S.REPATH_SECONDS
        self.guard.follow(self.path, delta_seconds, S.GUARD_CHASE_SPEED)

    def _lose_life(self, spawn) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.mode = "kalah"
            self.message = "Nyawa habis. Tekan R untuk mencoba lagi."
            return
        if hasattr(spawn, "x"):
            x, y = spawn.x, spawn.y
        else:
            x, y = spawn
        self.player.respawn(x, y)

    def _caught(self) -> None:
        """Pemain tersentuh penjaga: kehilangan nyawa dan penjaga diulang."""
        start = cell_center(self.lorong["start"])
        self._lose_life(start - pygame.Vector2(S.PLAYER_SIZE / 2,
                                               S.PLAYER_SIZE / 2))
        if self.mode != "lorong":
            return
        self.guard.position.update(cell_center(self.lorong["guard_start"]))
        self.guard.rect.center = (round(self.guard.position.x),
                                  round(self.guard.position.y))
        self.guard.set_state("idle")
        self.brain = GuardBrain(self.lorong["waypoints"])
        self.path = []
        self.repath_timer = 0.0

    # --- gambar -------------------------------------------------------
    def draw(self) -> None:
        self.screen.fill(S.BACKGROUND)
        if self.mode == "rak":
            self._draw_rak()
        elif self.mode == "lorong":
            self._draw_lorong()
        else:
            self._draw_end()
        self._draw_hud()

    def _draw_rak(self) -> None:
        self.solids.draw(self.screen)
        self.rak["artefacts"].draw(self.screen)
        self.rak["crates"].draw(self.screen)
        self.screen.blit(self.rak["door"].image, self.rak["door"].rect)
        self.screen.blit(self.player.image, self.player.rect)

    def _draw_lorong(self) -> None:
        for rect in self.lorong["wall_rects"]:
            pygame.draw.rect(self.screen, S.FLOOR_COLOR, rect)
        exit_pos = cell_center(self.lorong["exit"])
        pygame.draw.rect(self.screen, S.DOOR_COLOR,
                         pygame.Rect(exit_pos.x - S.CELL / 2 + 4,
                                     exit_pos.y - S.CELL / 2 + 4,
                                     S.CELL - 8, S.CELL - 8))
        if self.path and self.guard.state == CHASE:
            points = [(S.GRID_OFFSET_X + c[0] * S.CELL + S.CELL / 2,
                       S.GRID_OFFSET_Y + c[1] * S.CELL + S.CELL / 2)
                      for c in self.path]
            pygame.draw.lines(self.screen, S.PATH_COLOR, False, points, 3)
        if self.guard.state == CHASE:
            pygame.draw.line(self.screen, S.GUARD_CHASE_COLOR,
                             self.guard.position, self.player.position, 2)
        self.screen.blit(self.player.image, self.player.rect)
        pygame.draw.polygon(self.screen, S.ARTEFACT_COLOR,
                            [(self.player.rect.centerx,
                              self.player.rect.top - 12),
                             (self.player.rect.centerx + 7,
                              self.player.rect.top - 5),
                             (self.player.rect.centerx,
                              self.player.rect.top + 2),
                             (self.player.rect.centerx - 7,
                              self.player.rect.top - 5)])
        self.screen.blit(self.guard.image, self.guard.rect)

    def _draw_end(self) -> None:
        self.screen.blit(self.player.image, self.player.rect)
        text = self.font.render(self.message, True, S.TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(S.WINDOW_WIDTH // 2,
                                                     300)))

    def _draw_hud(self) -> None:
        judul = "Gudang Artefak"
        if self.mode == "rak":
            judul += " - Rak"
        elif self.mode == "lorong":
            judul += " - Lorong"
        self.screen.blit(self.font.render(judul, True, S.TEXT_COLOR), (24, 18))
        info = f"Skor {self.score}   Nyawa {self.lives}"
        self.screen.blit(self.small.render(info, True, S.ARTEFACT_COLOR),
                         (24, 46))
        if self.mode == "lorong" and self.guard is not None:
            status = f"Penjaga: {self.guard.state}"
            self.screen.blit(self.small.render(status, True, S.HINT_COLOR),
                             (760, 46))
