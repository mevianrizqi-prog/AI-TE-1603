"""Antarmuka Tkinter untuk EvacRoute AI."""
import tkinter as tk
from tkinter import ttk

from expert_system import diagnose
from search_algorithm import ALGORITHMS, BuildingGraph

COLOR_STATUS = {"AMAN": "#1b873f", "WASPADA": "#b7791f", "BAHAYA": "#c53030"}
SCALE, MARGIN = 10, 35


class App(tk.Tk):
    def __init__(self, graph: BuildingGraph):
        super().__init__()
        self.title("EvacRoute AI - Diagnosis Rute Evakuasi Gedung")
        self.graph = graph
        self.name_to_id = {n.name: i for i, n in graph.nodes.items()}
        self._build_controls()
        self._build_canvases()
        self._build_output()
        self.draw()

    # ---------- tata letak ----------
    def _build_controls(self):
        f = ttk.Frame(self, padding=8)
        f.pack(fill="x")
        ttk.Label(f, text="Lokasi Anda:").grid(row=0, column=0, sticky="w")
        self.start_var = tk.StringVar(value="Lab Komputer")
        ttk.Combobox(f, textvariable=self.start_var, values=list(self.name_to_id),
                     state="readonly", width=22).grid(row=0, column=1, padx=6)
        ttk.Label(f, text="Algoritma:").grid(row=1, column=0, sticky="w", pady=4)
        self.algo_var = tk.StringVar(value="BFS")
        ttk.Combobox(f, textvariable=self.algo_var, values=list(ALGORITHMS),
                     state="readonly", width=22).grid(row=1, column=1, padx=6)
        ttk.Label(f, text="Area terdampak bahaya\n(boleh pilih lebih dari satu):").grid(row=0, column=2, rowspan=2, padx=12)
        self.hazards = tk.Listbox(f, selectmode=tk.MULTIPLE, height=4, exportselection=False, width=24)
        for name in self.name_to_id:
            self.hazards.insert(tk.END, name)
        self.hazards.grid(row=0, column=3, rowspan=2)
        sb = ttk.Scrollbar(f, command=self.hazards.yview)
        self.hazards.config(yscrollcommand=sb.set)
        sb.grid(row=0, column=4, rowspan=2, sticky="ns")
        ttk.Button(f, text="Diagnosa", command=self.run).grid(row=0, column=5, padx=10)
        ttk.Button(f, text="Reset", command=self.reset).grid(row=1, column=5, padx=10)

    def _build_canvases(self):
        f = ttk.Frame(self)
        f.pack(padx=8)
        self.canvases = {}
        for col, floor in enumerate((1, 2)):
            ttk.Label(f, text=f"Lantai {floor}").grid(row=0, column=col)
            cv = tk.Canvas(f, width=40 * SCALE + 2 * MARGIN + 20, height=20 * SCALE + 2 * MARGIN,
                           bg="white", highlightthickness=1, highlightbackground="#999")
            cv.grid(row=1, column=col, padx=4, pady=4)
            self.canvases[floor] = cv
        ttk.Label(f, text="Hijau = pintu keluar | Merah = bahaya | Biru = lokasi Anda | Kuning/garis merah = rute",
                  font=("Arial", 8)).grid(row=2, column=0, columnspan=2)

    def _build_output(self):
        f = ttk.Frame(self, padding=8)
        f.pack(fill="both", expand=True)
        self.status_lbl = tk.Label(f, text="Status: -", font=("Arial", 14, "bold"))
        self.status_lbl.pack(anchor="w")
        self.output = tk.Text(f, height=9, width=95, wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True)

    # ---------- aksi ----------
    def selected_blocked(self):
        return {self.name_to_id[self.hazards.get(i)] for i in self.hazards.curselection()}

    def run(self):
        start = self.name_to_id[self.start_var.get()]
        blocked = self.selected_blocked()
        d = diagnose(self.graph, start, blocked, self.algo_var.get())
        self.status_lbl.config(text=f"Status: {d.status}", fg=COLOR_STATUS[d.status])
        lines = []
        if d.result.found:
            lines.append("Rute: " + " -> ".join(d.path_names))
            lines.append(f"Jarak: {d.result.distance} m | Langkah: {d.result.hops} | "
                         f"Node diekspansi: {d.result.expanded} ({d.result.algorithm})")
        else:
            lines.append("Rute: tidak ditemukan")
        lines.append("")
        lines.append("Saran / hasil aturan:")
        lines += [f"- {m}" for m in d.messages]
        self._write("\n".join(lines))
        self.draw(d, start, blocked)

    def reset(self):
        self.hazards.selection_clear(0, tk.END)
        self.status_lbl.config(text="Status: -", fg="black")
        self._write("")
        self.draw()

    def _write(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")

    # ---------- gambar denah ----------
    def draw(self, d=None, start=None, blocked=()):
        path = d.result.path if d and d.result.found else []
        path_edges = {frozenset(e) for e in zip(path, path[1:])}
        for floor, cv in self.canvases.items():
            cv.delete("all")
            nodes = [n for n in self.graph.nodes.values() if n.floor == floor]
            y0 = min(n.y for n in nodes)
            pos = {n.id: (MARGIN + n.x * SCALE, MARGIN + (n.y - y0) * SCALE) for n in nodes}
            for a in pos:
                for b in self.graph.adj[a]:
                    if b in pos and a < b:
                        on_path = frozenset((a, b)) in path_edges
                        cv.create_line(*pos[a], *pos[b], fill="#e53e3e" if on_path else "#a0aec0",
                                       width=3 if on_path else 1)
            for n in nodes:
                x, y = pos[n.id]
                fill = "#e2e8f0"
                if n.id in path:
                    fill = "#f6e05e"
                if n.is_exit:
                    fill = "#48bb78"
                if n.id in blocked:
                    fill = "#e53e3e"
                outline, width = ("#2b6cb0", 3) if n.id == start else ("#4a5568", 1)
                cv.create_oval(x - 7, y - 7, x + 7, y + 7, fill=fill, outline=outline, width=width)
                cv.create_text(x, y + 15, text=n.name, font=("Arial", 7))


def launch(graph: BuildingGraph):
    App(graph).mainloop()
