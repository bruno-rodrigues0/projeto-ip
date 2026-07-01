import pygame
from core.constants import ROOT_DIR
from entities.enemy_attack import EnemyAttack, Projectile

# png luva
S_LUVA = pygame.image.load(ROOT_DIR / "src/assets/img/luvamj.png").convert_alpha()
S_LUVA = pygame.transform.scale(S_LUVA, (40, 40))   # tamanho


TOPO = 150        # altura onde a luva aparece
FUNDO = 560       #  passar disso, a luva volta pro topo
ATRASO_SEGUNDA_CHUVA = 3.0   # quando troca da primeira pra segunda chuva


class ProjetilDireita(Projectile):
    #cai pra direita

    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.x_inicial = x   #reposicionamento

    def move(self, dt: float) -> None:
        self.vy = 420
        self.vx = 230
        #recomeca
        if self.y > FUNDO:
            self.y = TOPO
            self.x = self.x_inicial


class ProjetilEsquerda(Projectile):
    #cai pra esquerda

    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.x_inicial = x

    def move(self, dt: float) -> None:
        self.vy = 420
        self.vx = -210
        if self.y > FUNDO:
            self.y = TOPO
            self.x = self.x_inicial


class Attack12(EnemyAttack):
    attack_time = 2   # duração do ataque

    def __init__(self) -> None:
        super().__init__()
        self.tempo = 0.0
        self.segunda_chuva_ativa = False
        self.create_projectiles()

    def create_projectiles(self) -> None:
        # primeira chuva
        posicoes_dir = [315, 395, 475, 555, 635, 715]
        for x in posicoes_dir:
            projetil = ProjetilDireita(S_LUVA, x, TOPO)
            self.projectiles.append(projetil)

    def update(self, dt: float) -> None:
        self.tempo += dt

        # segunda chuva (tira a primeira e coloca a segunda)
        if self.tempo >= ATRASO_SEGUNDA_CHUVA and not self.segunda_chuva_ativa:
            self.segunda_chuva_ativa = True
            self.projectiles.clear()   # some com a primeira chuva
            posicoes_esq = [485, 565, 645, 725, 805, 885]
            for x in posicoes_esq:
                projetil = ProjetilEsquerda(S_LUVA, x, TOPO)
                self.projectiles.append(projetil)

        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)