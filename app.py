import reflex as rx
import random
import math

# ── Palette & constants ────────────────────────────────────────────────────────
COLORS = {
    "soil":      "#3B2314",
    "bark":      "#6B4226",
    "leaf_dark": "#2D6A4F",
    "leaf_mid":  "#52B788",
    "leaf_light":"#95D5B2",
    "bloom":     "#F4845F",
    "petal":     "#F7B267",
    "sky_top":   "#0B132B",
    "sky_bot":   "#1C3144",
    "moon":      "#F0E68C",
    "star":      "#FFFACD",
    "gold":      "#FFD700",
    "xp_bar":    "#52B788",
    "xp_bg":     "#1C3144",
    "text_main": "#E8F5E9",
    "text_sub":  "#95D5B2",
}

SEED_MESSAGES = [
    "🌱 A seed stirs in the dark...",
    "🌿 Roots reach deeper.",
    "🍃 Sunlight calls the shoot upward.",
    "🌸 A bud swells with potential.",
    "🌺 Petals unfurl to the world.",
    "🌳 The trunk remembers every storm.",
    "✨ Your garden breathes.",
    "🌙 Even at night, roots grow.",
    "💧 One drop feeds a forest.",
    "🔥 The ancient tree awakens.",
]

LEVEL_NAMES = [
    "Bare Soil",        # 1
    "Seedling",         # 2
    "Sprouting",        # 3
    "Sapling",          # 4
    "Young Tree",       # 5
    "Grove Keeper",     # 6
    "Forest Tender",    # 7
    "Elder Botanist",   # 8
    "Canopy Master",    # 9
    "Ancient Gardener", # 10
]

TREE_STAGES = [
    "🌑",   # 1 – nothing
    "🌱",   # 2
    "🪴",   # 3
    "🌿",   # 4
    "🌾",   # 5
    "🎋",   # 6
    "🌲",   # 7
    "🌳",   # 8
    "🌴",   # 9
    "🎄",   # 10+
]

XP_PER_LEVEL = 100


# ── State ──────────────────────────────────────────────────────────────────────
class State(rx.State):
    blooms: int = 0
    level: int = 1
    xp: int = 0
    coins: int = 0
    streak: int = 0
    message: str = "Welcome, Gardener. Plant your first seed."
    last_bonus: str = ""
    garden: list[str] = []          # emoji plants collected
    achievements: list[str] = []    # unlocked achievements
    show_levelup: bool = False
    show_achievement: bool = False
    achievement_text: str = ""
    particles: list[dict] = []      # floating particle data
    total_clicks: int = 0

    # ── computed vars ────────────────────────────────────────────────────────
    @rx.var
    def xp_percent(self) -> int:
        return min(int((self.xp / XP_PER_LEVEL) * 100), 100)

    @rx.var
    def xp_width(self) -> str:
        return f"{self.xp_percent}%"

    @rx.var
    def level_name(self) -> str:
        idx = min(self.level - 1, len(LEVEL_NAMES) - 1)
        return LEVEL_NAMES[idx]

    @rx.var
    def tree_emoji(self) -> str:
        idx = min(self.level - 1, len(TREE_STAGES) - 1)
        return TREE_STAGES[idx]

    @rx.var
    def garden_preview(self) -> list[str]:
        return self.garden[-12:] if len(self.garden) > 12 else self.garden

    @rx.var
    def achievement_count(self) -> int:
        return len(self.achievements)

    # ── actions ──────────────────────────────────────────────────────────────
    def plant_seed(self):
        self.total_clicks += 1
        self.blooms += 1
        self.streak += 1

        # Coin drop (random bonus)
        coin_bonus = random.choice([1, 1, 1, 2, 2, 3, 5])
        self.coins += coin_bonus

        # XP gain (streak multiplier)
        streak_mult = min(self.streak // 5 + 1, 4)
        xp_gain = 20 * streak_mult
        self.xp += xp_gain
        self.last_bonus = f"+{xp_gain} XP" + (f" × {streak_mult} streak!" if streak_mult > 1 else "")

        # Plant a random garden emoji
        plant_pool = ["🌷","🌹","🌺","🌸","🌼","🌻","🪷","🌿","🍀","🎋","🌴","🌲","🌳","🎄","🪴","🎍","🪸","🌾","🍃","🍂","🌵","🌡","🎑","🪨","🏵"]
        self.garden.append(random.choice(plant_pool))

        # Message
        self.message = random.choice(SEED_MESSAGES)

        # Check achievements
        self._check_achievements()

        # Level up logic
        if self.xp >= XP_PER_LEVEL:
            self.level += 1
            self.xp = self.xp - XP_PER_LEVEL
            self.show_levelup = True
            self.message = f"🎉 LEVEL {self.level} — {self.level_name}!"

    def _check_achievements(self):
        newly_unlocked = []
        if self.blooms == 1 and "First Bloom" not in self.achievements:
            newly_unlocked.append("🌱 First Bloom")
        if self.blooms == 10 and "Ten Blooms" not in self.achievements:
            newly_unlocked.append("🌿 Ten Blooms")
        if self.blooms == 50 and "Fifty Blooms" not in self.achievements:
            newly_unlocked.append("🌸 Fifty Blooms")
        if self.coins >= 50 and "Coin Hoarder" not in self.achievements:
            newly_unlocked.append("🪙 Coin Hoarder")
        if self.level >= 3 and "Sapling Spirit" not in self.achievements:
            newly_unlocked.append("🌲 Sapling Spirit")
        if self.streak >= 10 and "On Fire" not in self.achievements:
            newly_unlocked.append("🔥 On Fire")
        if self.level >= 5 and "Grove Master" not in self.achievements:
            newly_unlocked.append("🌳 Grove Master")
        if self.total_clicks >= 100 and "Century Gardener" not in self.achievements:
            newly_unlocked.append("💯 Century Gardener")
        for a in newly_unlocked:
            self.achievements.append(a)
            self.achievement_text = a
            self.show_achievement = True

    def dismiss_levelup(self):
        self.show_levelup = False

    def dismiss_achievement(self):
        self.show_achievement = False

    def reset_streak(self):
        self.streak = 0
        self.message = "Streak reset. Start fresh! 🌱"


# ── Helpers for UI blocks ──────────────────────────────────────────────────────
def stat_card(icon: str, label: str, value) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(icon, font_size="1.6em"),
            rx.text(value, font_size="1.4em", font_weight="800", color=COLORS["leaf_light"]),
            rx.text(label, font_size="0.65em", color=COLORS["text_sub"], letter_spacing="0.1em", text_transform="uppercase"),
            spacing="1", align="center",
        ),
        bg="rgba(11,19,43,0.6)",
        border=f"1px solid {COLORS['leaf_mid']}33",
        border_radius="16px",
        padding="1em 1.4em",
        backdrop_filter="blur(8px)",
        box_shadow=f"0 4px 24px rgba(0,0,0,0.35)",
        min_width="90px",
    )


def xp_bar() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(
                width=State.xp_width,
                height="100%",
                bg=f"linear-gradient(90deg, {COLORS['leaf_mid']}, {COLORS['leaf_light']})",
                border_radius="20px",
                transition="width 0.6s cubic-bezier(.22,1,.36,1)",
                box_shadow=f"0 0 12px {COLORS['leaf_mid']}99",
            ),
            width="100%",
            height="14px",
            bg=COLORS["xp_bg"],
            border_radius="20px",
            overflow="hidden",
            border=f"1px solid {COLORS['leaf_mid']}44",
        ),
        rx.hstack(
            rx.text(f"XP", font_size="0.7em", color=COLORS["text_sub"]),
            rx.spacer(),
            rx.text(State.xp_percent, "/100", font_size="0.7em", color=COLORS["text_sub"]),
        ),
        width="300px",
    )


def tree_display() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text(
                State.tree_emoji,
                font_size="7em",
                style={
                    "filter": "drop-shadow(0 0 24px #52B78888)",
                    "animation": "treepulse 3s ease-in-out infinite",
                },
            ),
            rx.text(
                State.level_name,
                font_size="0.85em",
                color=COLORS["text_sub"],
                letter_spacing="0.18em",
                text_transform="uppercase",
                font_weight="600",
            ),
            spacing="2",
            align="center",
        ),
        width="180px",
        height="180px",
        border_radius="50%",
        bg="radial-gradient(circle, #1C314488 60%, transparent 100%)",
        border=f"2px solid {COLORS['leaf_mid']}44",
        box_shadow=f"0 0 40px {COLORS['leaf_dark']}66",
    )


def bloom_button() -> rx.Component:
    return rx.button(
        rx.vstack(
            rx.text("🌸", font_size="2em"),
            rx.text("PLANT SEED", font_size="0.75em", font_weight="800", letter_spacing="0.15em"),
            spacing="1",
            align="center",
        ),
        on_click=State.plant_seed,
        width="160px",
        height="160px",
        border_radius="50%",
        bg=f"radial-gradient(circle, {COLORS['leaf_mid']}, {COLORS['leaf_dark']})",
        color=COLORS["text_main"],
        border=f"3px solid {COLORS['leaf_light']}88",
        box_shadow=f"0 0 32px {COLORS['leaf_mid']}88, 0 8px 32px rgba(0,0,0,0.4)",
        cursor="pointer",
        _hover={
            "transform": "scale(1.12)",
            "box_shadow": f"0 0 56px {COLORS['leaf_light']}cc, 0 8px 40px rgba(0,0,0,0.5)",
            "bg": f"radial-gradient(circle, {COLORS['leaf_light']}, {COLORS['leaf_mid']})",
        },
        _active={"transform": "scale(0.97)"},
        transition="all 0.25s cubic-bezier(.22,1,.36,1)",
    )


def garden_grid() -> rx.Component:
    return rx.box(
        rx.wrap(
            rx.foreach(
                State.garden_preview,
                lambda p: rx.text(
                    p,
                    font_size="1.6em",
                    style={"animation": "popin 0.4s cubic-bezier(.22,1,.36,1)"},
                ),
            ),
            spacing="2",
            justify="center",
        ),
        bg="rgba(11,19,43,0.55)",
        border=f"1px solid {COLORS['leaf_dark']}55",
        border_radius="20px",
        padding="1em 1.5em",
        min_height="60px",
        width="320px",
        backdrop_filter="blur(6px)",
    )


def achievement_chip(a: str) -> rx.Component:
    return rx.badge(
        a,
        variant="soft",
        color_scheme="grass",
        size="2",
        border_radius="20px",
    )


def level_up_modal() -> rx.Component:
    return rx.cond(
        State.show_levelup,
        rx.center(
            rx.vstack(
                rx.text("🎉", font_size="4em", style={"animation": "bounce 0.6s infinite alternate"}),
                rx.text("LEVEL UP!", font_size="2em", font_weight="900", color=COLORS["gold"],
                        style={"text_shadow": f"0 0 24px {COLORS['gold']}"}),
                rx.text(State.level_name, font_size="1.1em", color=COLORS["leaf_light"], letter_spacing="0.1em"),
                rx.button(
                    "Continue Growing 🌱",
                    on_click=State.dismiss_levelup,
                    bg=COLORS["leaf_mid"],
                    color="white",
                    border_radius="30px",
                    padding="0.6em 1.8em",
                    font_weight="700",
                    _hover={"bg": COLORS["leaf_light"], "color": COLORS["soil"]},
                ),
                spacing="4",
                align="center",
            ),
            position="fixed",
            top="0", left="0", right="0", bottom="0",
            bg="rgba(11,19,43,0.88)",
            z_index="100",
            style={"animation": "fadein 0.3s ease"},
        ),
        rx.box(),
    )


def achievement_toast() -> rx.Component:
    return rx.cond(
        State.show_achievement,
        rx.box(
            rx.hstack(
                rx.text("🏆", font_size="1.4em"),
                rx.vstack(
                    rx.text("Achievement Unlocked!", font_size="0.7em", color=COLORS["text_sub"], text_transform="uppercase"),
                    rx.text(State.achievement_text, font_size="1em", font_weight="700", color=COLORS["gold"]),
                    spacing="0",
                ),
                rx.button("✕", on_click=State.dismiss_achievement, variant="ghost", size="1", color=COLORS["text_sub"]),
                spacing="3", align="center",
            ),
            position="fixed",
            bottom="2em", right="2em",
            bg="rgba(11,19,43,0.92)",
            border=f"1px solid {COLORS['gold']}66",
            border_radius="16px",
            padding="1em 1.5em",
            box_shadow=f"0 0 24px {COLORS['gold']}44",
            z_index="99",
            style={"animation": "slidein 0.4s cubic-bezier(.22,1,.36,1)"},
        ),
        rx.box(),
    )


# ── Starfield background (pure CSS) ──────────────────────────────────────────
def starfield() -> rx.Component:
    # 30 star dots via inline CSS box-shadows
    stars = ", ".join(
        f"{random.randint(0,1440)}px {random.randint(0,900)}px #FFFACD"
        for _ in range(80)
    )
    return rx.box(
        width="2px", height="2px",
        bg="transparent",
        box_shadow=stars,
        border_radius="50%",
        position="absolute",
        top="0", left="0",
    )


# ── Main page ─────────────────────────────────────────────────────────────────
def index() -> rx.Component:
    keyframes = """
    @keyframes treepulse {
        0%,100% { transform: scale(1) rotate(-1deg); filter: drop-shadow(0 0 24px #52B78888); }
        50%      { transform: scale(1.07) rotate(1deg); filter: drop-shadow(0 0 40px #95D5B2cc); }
    }
    @keyframes popin {
        from { transform: scale(0) rotate(-15deg); opacity: 0; }
        to   { transform: scale(1) rotate(0); opacity: 1; }
    }
    @keyframes bounce {
        from { transform: translateY(0); }
        to   { transform: translateY(-12px); }
    }
    @keyframes fadein {
        from { opacity: 0; } to { opacity: 1; }
    }
    @keyframes slidein {
        from { transform: translateX(120px); opacity: 0; }
        to   { transform: translateX(0); opacity: 1; }
    }
    @keyframes twinkle {
        0%,100% { opacity: 1; } 50% { opacity: 0.3; }
    }
    @keyframes floatup {
        0%   { transform: translateY(0) scale(1); opacity: 1; }
        100% { transform: translateY(-80px) scale(0.6); opacity: 0; }
    }
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Nunito:wght@400;600;700;800&display=swap');
    body { font-family: 'Nunito', sans-serif; }
    """

    return rx.box(
        rx.html(f"<style>{keyframes}</style>"),

        # Starfield bg
        rx.box(
            starfield(),
            position="absolute", inset="0", overflow="hidden", z_index="0",
        ),

        # Moon
        rx.box(
            rx.text("🌕", font_size="3em", style={"filter": "drop-shadow(0 0 20px #F0E68Caa)"}),
            position="absolute", top="2em", right="4em", z_index="1",
        ),

        # Main content
        rx.center(
            rx.vstack(
                # ── Title ──
                rx.vstack(
                    rx.heading(
                        "MINDBLOOM",
                        font_family="'Cinzel Decorative', serif",
                        font_size=rx.breakpoints(initial="2em", md="3em"),
                        color=COLORS["leaf_light"],
                        style={"text_shadow": f"0 0 40px {COLORS['leaf_mid']}cc"},
                        letter_spacing="0.1em",
                    ),
                    rx.text(
                        "✦ The Living Garden of the Mind ✦",
                        font_size="0.8em",
                        color=COLORS["text_sub"],
                        letter_spacing="0.2em",
                    ),
                    spacing="1", align="center",
                ),

                # ── Stats row ──
                rx.hstack(
                    stat_card("🌸", "Blooms", State.blooms),
                    stat_card("⚡", "Level",  State.level),
                    stat_card("🪙", "Coins",  State.coins),
                    stat_card("🔥", "Streak", State.streak),
                    spacing="3", wrap="wrap", justify="center",
                ),

                # ── Tree + Button row ──
                rx.hstack(
                    tree_display(),
                    rx.vstack(
                        bloom_button(),
                        rx.text(
                            State.last_bonus,
                            font_size="0.8em",
                            color=COLORS["gold"],
                            font_weight="700",
                            min_height="1.2em",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    spacing="8",
                    align="center",
                    wrap="wrap",
                    justify="center",
                ),

                # ── Message ──
                rx.text(
                    State.message,
                    font_size="1em",
                    font_style="italic",
                    color=COLORS["text_sub"],
                    text_align="center",
                    max_width="320px",
                ),

                # ── XP bar ──
                rx.vstack(
                    rx.hstack(
                        rx.text("⚗️ Progress to next level", font_size="0.72em", color=COLORS["text_sub"]),
                        rx.spacer(),
                        rx.text(f"Level", font_size="0.72em", color=COLORS["text_sub"]),
                        rx.text(State.level, font_size="0.72em", color=COLORS["leaf_light"], font_weight="700"),
                        width="300px",
                    ),
                    xp_bar(),
                    spacing="1",
                    align="center",
                ),

                # ── Garden grid ──
                rx.vstack(
                    rx.text("🌿 Your Garden", font_size="0.75em", color=COLORS["text_sub"],
                            letter_spacing="0.15em", text_transform="uppercase"),
                    garden_grid(),
                    spacing="1", align="center",
                ),

                # ── Achievements ──
                rx.cond(
                    State.achievement_count > 0,
                    rx.vstack(
                        rx.text("🏆 Achievements", font_size="0.75em", color=COLORS["text_sub"],
                                letter_spacing="0.15em", text_transform="uppercase"),
                        rx.wrap(
                            rx.foreach(State.achievements, achievement_chip),
                            spacing="2", justify="center", max_width="340px",
                        ),
                        spacing="2", align="center",
                    ),
                    rx.box(),
                ),

                # ── Footer ──
                rx.hstack(
                    rx.text("Total seeds planted:", font_size="0.7em", color=COLORS["text_sub"]),
                    rx.text(State.total_clicks, font_size="0.7em", color=COLORS["leaf_light"], font_weight="700"),
                    rx.text("✦", color=COLORS["text_sub"], font_size="0.7em"),
                    rx.button(
                        "Reset Streak",
                        on_click=State.reset_streak,
                        size="1",
                        variant="ghost",
                        color=COLORS["bloom"],
                        font_size="0.7em",
                    ),
                    spacing="2", align="center",
                ),

                spacing="6",
                align="center",
                padding_y="3em",
                padding_x="1em",
                max_width="600px",
                width="100%",
            ),
            position="relative",
            z_index="2",
            width="100%",
            min_height="100vh",
        ),

        # Modals
        level_up_modal(),
        achievement_toast(),

        # Page wrapper
        position="relative",
        min_height="100vh",
        width="100%",
        background=f"linear-gradient(160deg, {COLORS['sky_top']} 0%, {COLORS['sky_bot']} 60%, {COLORS['leaf_dark']}55 100%)",
        overflow="hidden",
    )


# ── App bootstrap ─────────────────────────────────────────────────────────────
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=False,
        accent_color="grass",
        radius="large",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Nunito:wght@400;600;700;800&display=swap"
    ],
)
app.add_page(index, title="Mindbloom 🌸 — The Living Garden")
