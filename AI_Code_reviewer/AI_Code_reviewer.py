import reflex as rx
from typing import List, Dict
from database import insert_code, init_db
from code_analyzer import analyze_code_pipeline

# Initialize DB
init_db()

# ---------------- CODE STATE ---------------- #
from typing import List, Dict
import reflex as rx

class CodeState(rx.State):
    code_input: str = ""
    is_loading: bool = False

    # ✅ NEW: Language state
    language: str = "Python"

    unused_variables: List[str] = []
    infinite_loops: List[int] = []
    corrected_code: str = ""

    result: Dict[str, str] = {
        "status": "",
        "ai_suggestion": "",
    }

    def set_code_input(self, code: str):
        self.code_input = code

    # ✅ NEW: Set language from dropdown
    def set_language(self, value: str):
        self.language = value

    def analyze_code(self):
        if not self.code_input.strip():
            self.result = {
                "status": "error",
                "ai_suggestion": "Please enter code."
            }
            return

        self.is_loading = True

        try:
            # ✅ PASS language to backend
            analysis_result = analyze_code_pipeline(
                self.code_input,
                self.language   # <-- important
            )

            insert_code(self.code_input)

            self.unused_variables = analysis_result.get("unused_variables", [])
            self.infinite_loops = analysis_result.get("infinite_loops", [])
            self.corrected_code = analysis_result.get("corrected_code", "")

            ai_text = analysis_result.get("ai_suggestion", "")

            # ✅ SAFE CLEANING (avoid crash if text format changes)
            if "🔴 Syntax Errors" in ai_text:
                parts = ai_text.split("🔴 Syntax Errors")
                clean_text = "🔴 Syntax Errors" + parts[1]
            else:
                clean_text = ai_text

            self.result = {
                "status": "success",
                "ai_suggestion": clean_text
            }

        except Exception as e:
            self.result = {
                "status": "error",
                "ai_suggestion": str(e)
            }

        finally:
            self.is_loading = False

    async def handle_upload(self, files):
        file = files[0]
        content = await file.read()
        self.code_input = content.decode("utf-8")

#---------------------------------home
def home():
    return rx.vstack(
        navbar(),

        rx.center(
            rx.vstack(
                # 🔥 Title with glow + animation
                rx.heading(
                    " AI Code Reviewer",
                    size="9",
                    background="linear-gradient(90deg, #ff7e5f, #feb47b)",
                    background_clip="text",
                    color="transparent",
                    style={
                        "textShadow": "0px 0px 20px rgba(255,126,95,0.6)",
                        "animation": "fadeIn 1.5s ease-in-out"
                    }
                ),

                # ✨ Subtitle improved
                rx.text(
                    "Fix Bugs ⚡ Improve Code 🚀 Write Better Python 🐍",
                    font_size="18px",
                    color="lightgray",
                    text_align="center",
                    style={
                        "opacity": "0.85",
                        "animation": "fadeIn 2s ease-in-out"
                    }
                ),

                # 🚀 Buttons with hover effects
                rx.hstack(
                    rx.button(
                        "Start Analyzing 🔍",
                        on_click=rx.redirect("/analyzer"),
                        bg="linear-gradient(90deg, #ff7e5f, #feb47b)",
                        color="white",
                        size="3",
                        style={
                            "boxShadow": "0px 4px 15px rgba(255,126,95,0.4)",
                            "transition": "0.3s",
                        },
                        _hover={
                            "transform": "scale(1.08)",
                            "boxShadow": "0px 6px 20px rgba(255,126,95,0.7)"
                        }
                    ),

                    rx.button(
                        "View History 📜",
                        on_click=rx.redirect("/history"),
                        variant="outline",
                        color="white",
                        border="1px solid white",
                        size="3",
                        style={
                            "transition": "0.3s",
                        },
                        _hover={
                            "bg": "white",
                            "color": "#203a43",
                            "transform": "scale(1.08)"
                        }
                    ),
                    spacing="4"
                ),

                spacing="6",
                align="center"
            ),
            height="80vh",
            width="100%"
        ),

        # 🌌 Background + subtle overlay glow
        bg="linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        style={
            "backgroundImage": "radial-gradient(circle at top, rgba(255,126,95,0.15), transparent 70%)",
        },
        min_height="100vh"
    )
# ---------------- NAVBAR ---------------- #
def navbar():
    return rx.hstack(
        rx.text("⚡ AI Code Reviewer", font_weight="bold", font_size="20px", color="white"),
        rx.spacer(),
        rx.hstack(
            rx.link("Home", href="/", color="white"),
            rx.link("Analyzer", href="/analyzer", color="white"),
            rx.link("About", href="/about", color="white"),
            rx.link("History", href="/history", color="white"),
            spacing="6",
        ),
        padding="20px",
        width="100%",
        bg="linear-gradient(90deg, #6B73FF, #000DFF)",
    )
#--------about page--------
def about():
    return rx.vstack(
        navbar(),

        rx.center(
            rx.vstack(
                rx.heading("🚀 AI Code Reviewer", size="9", color="#ff8c66"),

                rx.text(
                    "Fix Bugs ⚡ Improve Code 🚀 Write Better Python 🐍",
                    color="#e2e8f0"
                ),

                rx.divider(width="60%", border_color="#475569"),

                rx.heading("📘 About", size="7", color="#f8fafc"),

                rx.text(
                    "This app analyzes Python code using AST and AI suggestions.",
                    text_align="center",
                    width="70%",
                    color="#e2e8f0"
                ),

                rx.heading("✨ Features", size="6", color="#f8fafc"),

                rx.vstack(
                    rx.text("✔ Syntax Error Detection", color="#38bdf8"),
                    rx.text("✔ Unused Variables", color="#38bdf8"),
                    rx.text("✔ Infinite Loop Detection", color="#38bdf8"),
                    rx.text("✔ AI Suggestions", color="#38bdf8"),
                    align="center"
                ),

                spacing="6",
                align="center",
                padding="40px"
            ),
            width="100%"
        ),

        bg="linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        min_height="100vh"
    )

from database import get_history


#-----------------HISTORY PAGE-----------------#
def history_page():
    history = get_history()

    return rx.vstack(
        navbar(),

        rx.center(
            rx.vstack(
                *[
                    rx.box(
                        rx.text(
                            f"ID: {item['id']} | Date: {item['created_at']}",
                            color="gray"
                        ),
                        rx.text(
                            item['code'],
                            font_family="monospace",
                            color="white",
                            white_space="pre-wrap"
                        ),
                        padding="15px",
                        margin_bottom="10px",
                        bg="#1e293b",
                        border_radius="10px",
                        width="80%"
                    )
                    for item in history
                ],
                spacing="4",
                align="center"
            ),
            padding="50px"
        ),

        bg="linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        min_height="100vh"
    )
# ---------------- RESULT SECTION ---------------- #
def result_section():
    return rx.vstack(

        # 🔴 AI ANALYSIS TEXT
        rx.heading("🧠 AI Analysis", color="#facc15"),

        rx.box(
            rx.text(
                CodeState.result["ai_suggestion"],
                white_space="pre-wrap",
                color="white"
            ),
            padding="15px",
            bg="#020617",
            border_radius="10px",
            width="100%"
        ),

        # 🟡 UNUSED VARIABLES
        rx.heading("🟡 Unused Variables", color="#facc15"),

        rx.cond(
            CodeState.unused_variables,
            rx.vstack(
                rx.foreach(
                    CodeState.unused_variables,
                    lambda item: rx.text(f"• {item}", color="yellow")
                )
            ),
            rx.text("None", color="gray")
        ),

        # 🔁 INFINITE LOOPS
        rx.heading("🔁 Infinite Loops", color="#f87171"),

        rx.cond(
            CodeState.infinite_loops,
            rx.vstack(
                rx.foreach(
                    CodeState.infinite_loops,
                    lambda item: rx.text(f"Line {item}", color="red")
                )
            ),
            rx.text("None", color="gray")
        ),

        # 📘 CORRECTED CODE
        rx.heading("📘 Corrected Code", color="#38bdf8"),

        rx.box(
            rx.text(
                CodeState.corrected_code,
                white_space="pre-wrap",
                font_family="monospace",
                color="#00ffcc"
            ),
            padding="15px",
            bg="#020617",
            border_radius="10px",
            width="100%"
        ),

        spacing="4",
        width="100%"
    )
# ---------------- ANALYZER PAGE ---------------- #
def analyzer_page():
    return rx.vstack(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("AI Code Analyzer", size="8", color="white"),
                rx.text("Paste your code and get instant AI-powered review.", color="gray"),

                # ✅ NEW: Language Dropdown (added cleanly)
                rx.select(
                    ["Python", "Java", "C", "C++", "JavaScript"],
                    placeholder="Select Language",
                    value=CodeState.language,
                    on_change=CodeState.set_language,
                    width="80%",
                    bg="#020617",
                    color="white",
                    border_radius="10px",
                ),

                rx.box(
                    rx.text_area(
                        placeholder="Paste your Python code here...",
                        value=CodeState.code_input,
                        on_change=CodeState.set_code_input,
                        width="100%",
                        height="300px",
                        bg="#020617",
                        color="white",
                        border_radius="10px",
                    ),
                    width="80%",
                    padding="20px",
                    bg="rgba(255,255,255,0.05)",
                    border_radius="15px",
                ),

                rx.hstack(
                    rx.button(
                        "⚡ Analyze Code",
                        on_click=CodeState.analyze_code,
                        bg="linear-gradient(90deg, #ff7e5f, #feb47b)",
                        color="white",
                    ),
                    rx.upload(
                        rx.button("📂 Upload File"),
                        on_drop=CodeState.handle_upload
                    ),
                    spacing="4",
                ),

                rx.cond(
                    CodeState.is_loading,
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("Analyzing...", color="white")
                    )
                ),

                rx.cond(
                    CodeState.result["status"] == "success",
                    rx.box(
                        result_section(),
                        width="80%",
                        padding="20px",
                        margin_top="20px",
                        bg="rgba(255,255,255,0.05)",
                        border_radius="15px",
                    )
                ),

                spacing="6",
                align="center",
            ),
            width="100%",
        ),
        bg="linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        min_height="100vh",
    )

# ---------------- APP ---------------- #

app = rx.App()

app.add_page(home, route="/")
app.add_page(analyzer_page, route="/analyzer")
app.add_page(about, route="/about")
app.add_page(history_page, route="/history")