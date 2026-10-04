# admin.py
# Admin command system for the Low-Risk Engine

from config import ADMIN_IDS

class AdminController:
    def __init__(self):
        self.running = True
        self.force_mines = False
        self.force_aviator = False

    def is_admin(self, user_id: int) -> bool:
        return user_id in ADMIN_IDS

    def handle_command(self, user_id: int, text: str) -> str | None:
        """
        Process admin commands.
        Returns a reply message or None if not an admin command.
        """
        if not self.is_admin(user_id):
            return None

        cmd = text.strip().lower()

        if cmd in ["/start_engine", "/start"]:
            self.running = True
            return "🟢 Engine started."

        if cmd in ["/stop_engine", "/stop"]:
            self.running = False
            return "🔴 Engine stopped. No more automatic signals."

        if cmd == "/status":
            state = "RUNNING" if self.running else "STOPPED"
            return f"🛠 Status: <b>{state}</b>"

        if cmd == "/force_mines":
            self.force_mines = True
            return "⚡ Force Mines signal queued."

        if cmd == "/force_aviator":
            self.force_aviator = True
            return "⚡ Force Aviator signal queued."

        if cmd == "/help_admin":
            return (
                "🛠 <b>Admin Commands</b>\n\n"
                "/start_engine – Start automatic signals\n"
                "/stop_engine – Stop automatic signals\n"
                "/status – Check engine status\n"
                "/force_mines – Send Mines signal now\n"
                "/force_aviator – Send Aviator signal now\n"
                "/help_admin – Show this message"
            )

        return None

    def consume_force_mines(self) -> bool:
        if self.force_mines:
            self.force_mines = False
            return True
        return False

    def consume_force_aviator(self) -> bool:
        if self.force_aviator:
            self.force_aviator = False
            return True
        return False
