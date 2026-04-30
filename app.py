import reflex as rx
import random

class State(rx.State):
    """The game logic in pure Python."""
    blooms: int = 0
    level: int = 1
    xp: int = 0
    message: str = "Welcome, Gardener. Ready to grow?"
    
    @rx.var
    def progress_width(self) -> str:
        # Calculate progress bar width based on XP
        return f"{self.xp}%"

    def plant_seed(self):
        self.blooms += 1
        self.xp += 20
        
        # Level up logic
        if self.xp >= 100:
            self.level += 1
            self.xp = 0
            self.message = f"Level {self.level}! Your mind is expanding."
        else:
            messages = ["Focusing...", "Nurturing...", "Blooming...", "Peaceful."]
            self.message = random.choice(messages)

def index():
    return rx.center(
        rx.vstack(
            # Header Section
            rx.heading("Mindbloom", size="9", color="#5A639C"),
            rx.text(self.message, font_style="italic", color="#777"),
            
            # The "Gamified" Stats
            rx.hbox(
                rx.badge(f"Level {State.level}", variant="soft", color_scheme="purple", size="3"),
                rx.badge(f"Blooms: {State.blooms}", variant="soft", color_scheme="grass", size="3"),
                spacing="4",
            ),
            
            # The Bloom Progress Bar
            rx.box(
                rx.box(
                    width=State.progress_width,
                    height="100%",
                    bg="#9ED2BE", # Pastel Mint
                    transition="width 0.5s ease-in-out",
                    border_radius="15px",
                ),
                width="300px",
                height="20px",
                bg="#E5E0FF", # Soft Lavender
                border_radius="15px",
                overflow="hidden",
                border="2px solid #D7E5CA",
            ),

            # The Main Action Button
            rx.button(
                "Click to Bloom",
                on_click=State.plant_seed,
                size="4",
                padding="2em",
                border_radius="50%",
                bg="#9ED2BE",
                _hover={"transform": "scale(1.1)", "bg": "#7EAA92"},
                transition="all 0.3s ease",
                color="white",
                box_shadow="0px 10px 20px rgba(0,0,0,0.1)",
            ),
            
            spacing="7",
            align="center",
        ),
        # Background Styling
        width="100%",
        height="100vh",
        background="linear-gradient(135deg, #FFF2F2 0%, #E5E0FF 50%, #D7E5CA 100%)",
    )

app = rx.App(
    theme=rx.theme(
        appearance="light", 
        has_background=True, 
        accent_color="grass"
    )
)
app.add_page(index)
