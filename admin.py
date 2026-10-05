# admin.py — AI Engine v4 Admin Controller

from config import ADMIN_IDS, DEFAULT_MODE, DEFAULT_INTENSITY

class AdminController:
    def __init__(self):
        self.running = True
        self.mode = DEFAULT_MODE              # safe | normal
        self.intensity = DEFAULT_INTENSITY    # normal | aggressive
        self.force_mines = False
        self.force_crash = False
        self.maintenance = False

    def is_admin(self, user_id: int) -> bool:
        return user_id in ADMIN_IDS

    def handle(self, user_id: int, text: str) -> str | None:
        if not self.is_admin(user_id):
            return None

        cmd = text.strip().lower()

        if cmd in ["/start_engine", "/start"]:
            self.running = True
            self.maintenance = False
            return "🟢 Engine started."

        if cmd in ["/stop_engine", "/stop"]:
            self.running = False
            return "🔴 Engine stopped."

        if cmd == "/status":
            state = "RUNNING" if self.running else "STOPPED"
            maint = " | MAINTENANCE" if self.maintenance else ""
            return (
                f"🛠 <b>Status</b>\n"
                f"Engine: <b>{state}{maint}</b>\n"
                f"Mode: <b>{self.mode.upper()}</b>\n"
                f"Intensity: <b>{self.intensity.upper()}</b>"
            )

        if cmd == "/mode_safe":
            self.mode = "safe"
            return "모드 changed → <b>SAFE</b> (very low risk)"

        if cmd == "/mode_normal":
            self.mode = "normal"
            return "Mode changed → <b>NORMAL</b>"

        if cmd == "/intensity_normal":
            self.intensity = "normal"
            return "Intensity → <b>NORMAL</b>"

        if cmd == "/intensity_aggressive":
            self.intensity = "aggressive"
            return "Intensity → <b>AGGRESSIVE</b> (faster signals)"

        if cmd == "/force_mines":
            self.force_mines = True
            return "⚡ Force Mines signal queued."

        if cmd == "/force_crash":
            self.force_crash = True
            return "⚡ Force Crash signal queued."

        if cmd == "/maintenance_on":
            self.maintenance = True
            self.running = False
            return "🔧 Maintenance mode ON. Engine paused."

        if cmd == "/maintenance_off":
            self.maintenance = False
            self.running = True
            return "🔧 Maintenance mode OFF. Engine resumed."

        if cmd == "/help_admin":
            return (
                "🛠 <b>Admin Commands v4</b>\n\n"
                "/start_engine – Start\n"
                "/stop_engine – Stop\n"
                "/status – Full status\n"
                "/mode_safe – Very low risk\n"
                "/mode_normal – Normal low risk\n"
                "/intensity_normal – Normal speed\n"
                "/intensity_aggressive – Faster signals\n"
                "/force_mines – Send Mines now\n"
                "/force_crash – Send Crash now\n"
                "/maintenance_on – Pause everything\n"
                "/maintenance_off – Resume\n"
                "/help_admin – This menu"
            )

        return None

    def consume_force_mines(self) -> bool:
        if self.force_mines:
            self.force_mines = False
            return True
        return False

    def consume_force_crash(self) -> bool:
        if self.force_crash:
            self.force_crash = False
            return True
        return False
