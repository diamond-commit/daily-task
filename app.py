
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from pathlib import Path
import json
import html

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "tasks.json"
HTML_FILE = BASE_DIR / "templates" / "index.html"


def load_tasks():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


class DailyTrackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        tasks = load_tasks()

        task_items = ""

        for task in tasks:
            task_items += f"""
                <li class="bg-slate-800 p-4 rounded-xl mb-3">
                    {html.escape(task)}
                </li>
            """

        with open(HTML_FILE, "r", encoding="utf-8") as file:
            page = file.read()

        page = page.replace("{{ tasks }}", task_items)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length).decode("utf-8")

        form_data = parse_qs(body)
        task = form_data.get("task", [""])[0].strip()

        if task:
            tasks = load_tasks()
            tasks.append(task)
            save_tasks(tasks)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


server = HTTPServer(("localhost", 8000), DailyTrackHandler)

print("DailyTrack is running at http://localhost:8000")

server.serve_forever()
