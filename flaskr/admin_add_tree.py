import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

TREES_PATH = os.path.join(os.path.dirname(__file__), "trees.json")

def load_trees():
    if not os.path.exists(TREES_PATH):
        return []
    with open(TREES_PATH, encoding="utf-8") as f:
        return json.load(f)

def save_trees(trees):
    with open(TREES_PATH, "w", encoding="utf-8") as f:
        json.dump(trees, f, ensure_ascii=False, indent=2)

class TreeAdminApp:
    def __init__(self, root):
        self.root = root
        root.title("Adicionar/Editar Árvore")
        root.geometry("900x700")
        root.configure(bg="#f5f5f5")

        self.trees = load_trees()
        self.editing_index = None
        self.filtered_indices = []

        # --- Search and List Frame ---
        list_frame = tk.Frame(root, bg="#f5f5f5")
        list_frame.pack(fill="x", padx=10, pady=8)

        tk.Label(list_frame, text="Buscar árvore:", bg="#f5f5f5", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.search_entry = tk.Entry(list_frame, width=30)
        self.search_entry.grid(row=0, column=1, sticky="w", padx=4)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_trees_listbox())

        tk.Label(list_frame, text="Árvores cadastradas:", bg="#f5f5f5", font=("Arial", 11, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8,0))
        self.trees_listbox = tk.Listbox(list_frame, height=10, width=60, font=("Arial", 11))
        self.trees_listbox.grid(row=2, column=0, columnspan=2, sticky="w")
        self.trees_listbox.bind('<<ListboxSelect>>', self.on_tree_select)

        btns_frame = tk.Frame(list_frame, bg="#f5f5f5")
        btns_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=4)
        tk.Button(btns_frame, text="Remover Selecionada", command=self.remove_selected_tree, bg="#e57373", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=2)
        tk.Button(btns_frame, text="Editar Selecionada", command=self.edit_selected_tree, bg="#64b5f6", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=2)

        # --- Form Frame ---
        form_frame = tk.Frame(root, bg="#f5f5f5")
        form_frame.pack(fill="both", expand=True, padx=10, pady=8)

        # Number and Name
        tk.Label(form_frame, text="Número da árvore (único):", bg="#f5f5f5", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.number_entry = tk.Entry(form_frame, width=10, font=("Arial", 11))
        self.number_entry.grid(row=0, column=1, sticky="w", padx=4)

        tk.Label(form_frame, text="Nome da árvore:", bg="#f5f5f5", font=("Arial", 11)).grid(row=0, column=2, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.name_entry.grid(row=0, column=3, sticky="w", padx=4)

        # Hints
        tk.Label(form_frame, text="Dicas da árvore:", bg="#f5f5f5", font=("Arial", 11)).grid(row=1, column=0, sticky="nw", pady=(10,0))
        self.hints_listbox = tk.Listbox(form_frame, height=4, width=40, font=("Arial", 11))
        self.hints_listbox.grid(row=1, column=1, sticky="w", pady=(10,0))
        self.hint_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.hint_entry.grid(row=2, column=1, sticky="w")
        hint_btns = tk.Frame(form_frame, bg="#f5f5f5")
        hint_btns.grid(row=3, column=1, sticky="w")
        tk.Button(hint_btns, text="Adicionar Dica", command=self.add_hint, bg="#81c784", font=("Arial", 10)).pack(side="left", padx=2)
        tk.Button(hint_btns, text="Editar Dica", command=self.edit_hint, bg="#64b5f6", font=("Arial", 10)).pack(side="left", padx=2)
        tk.Button(hint_btns, text="Remover Dica", command=self.remove_hint, bg="#e57373", font=("Arial", 10)).pack(side="left", padx=2)

        # Comments
        tk.Label(form_frame, text="Comentários sobre a árvore:", bg="#f5f5f5", font=("Arial", 11)).grid(row=1, column=2, sticky="nw", pady=(10,0))
        self.comments_listbox = tk.Listbox(form_frame, height=4, width=40, font=("Arial", 11))
        self.comments_listbox.grid(row=1, column=3, sticky="w", pady=(10,0))
        self.comment_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.comment_entry.grid(row=2, column=3, sticky="w")
        comment_btns = tk.Frame(form_frame, bg="#f5f5f5")
        comment_btns.grid(row=3, column=3, sticky="w")
        tk.Button(comment_btns, text="Adicionar Comentário", command=self.add_comment, bg="#81c784", font=("Arial", 10)).pack(side="left", padx=2)
        tk.Button(comment_btns, text="Editar Comentário", command=self.edit_comment, bg="#64b5f6", font=("Arial", 10)).pack(side="left", padx=2)
        tk.Button(comment_btns, text="Remover Comentário", command=self.remove_comment, bg="#e57373", font=("Arial", 10)).pack(side="left", padx=2)

        # Latitude/Longitude
        tk.Label(form_frame, text="Latitude:", bg="#f5f5f5", font=("Arial", 11)).grid(row=4, column=0, sticky="w", pady=(16,0))
        self.lat_entry = tk.Entry(form_frame, width=15, font=("Arial", 11))
        self.lat_entry.grid(row=4, column=1, sticky="w", pady=(16,0))
        tk.Label(form_frame, text="Longitude:", bg="#f5f5f5", font=("Arial", 11)).grid(row=4, column=2, sticky="w", pady=(16,0))
        self.lng_entry = tk.Entry(form_frame, width=15, font=("Arial", 11))
        self.lng_entry.grid(row=4, column=3, sticky="w", pady=(16,0))

        # Save buttons
        save_btns = tk.Frame(form_frame, bg="#f5f5f5")
        save_btns.grid(row=5, column=0, columnspan=4, pady=18)
        tk.Button(save_btns, text="Salvar Nova Árvore", command=self.save_tree, bg="#388e3c", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=8)
        tk.Button(save_btns, text="Salvar Alterações", command=self.save_edit_tree, bg="#1976d2", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=8)

        self.refresh_trees_listbox()

    def refresh_trees_listbox(self):
        search = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""
        # Sort trees by number
        sorted_trees = sorted(enumerate(self.trees), key=lambda x: x[1].get("number", 0))
        self.trees_listbox.delete(0, tk.END)
        self.filtered_indices = []
        for idx, tree in sorted_trees:
            name = tree.get("name", "")
            number = tree.get("number", "")
            display = f"{number}: {name}"
            if search in str(number).lower() or search in name.lower():
                self.trees_listbox.insert(tk.END, display)
                self.filtered_indices.append(idx)

    def add_hint(self):
        hint = self.hint_entry.get().strip()
        if hint:
            self.hints_listbox.insert(tk.END, hint)
            self.hint_entry.delete(0, tk.END)

    def edit_hint(self):
        selection = self.hints_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma dica para editar.")
            return
        idx = selection[0]
        new_hint = simpledialog.askstring("Editar Dica", "Nova dica:", initialvalue=self.hints_listbox.get(idx))
        if new_hint is not None:
            self.hints_listbox.delete(idx)
            self.hints_listbox.insert(idx, new_hint)

    def remove_hint(self):
        selection = self.hints_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma dica para remover.")
            return
        idx = selection[0]
        self.hints_listbox.delete(idx)

    def add_comment(self):
        comment = self.comment_entry.get().strip()
        if comment:
            self.comments_listbox.insert(tk.END, comment)
            self.comment_entry.delete(0, tk.END)

    def edit_comment(self):
        selection = self.comments_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um comentário para editar.")
            return
        idx = selection[0]
        new_comment = simpledialog.askstring("Editar Comentário", "Novo comentário:", initialvalue=self.comments_listbox.get(idx))
        if new_comment is not None:
            self.comments_listbox.delete(idx)
            self.comments_listbox.insert(idx, new_comment)

    def remove_comment(self):
        selection = self.comments_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um comentário para remover.")
            return
        idx = selection[0]
        self.comments_listbox.delete(idx)

    def save_tree(self):
        try:
            number = int(self.number_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Número inválido.")
            return
        if any(tree["number"] == number for tree in self.trees):
            messagebox.showerror("Erro", "Já existe uma árvore com esse número.")
            return
        name = self.name_entry.get().strip()
        hints = [self.hints_listbox.get(i) for i in range(self.hints_listbox.size())]
        comments = [self.comments_listbox.get(i) for i in range(self.comments_listbox.size())]
        try:
            lat = float(self.lat_entry.get().strip())
            lng = float(self.lng_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Coordenadas inválidas.")
            return
        tree = {
            "number": number,
            "name": name,
            "hints": hints,
            "comments": comments,
            "coordinates": {"lat": lat, "lng": lng}
        }
        self.trees.append(tree)
        save_trees(self.trees)
        messagebox.showinfo("Sucesso", "Árvore adicionada com sucesso!")
        self.clear_fields()
        self.refresh_trees_listbox()

    def save_edit_tree(self):
        if self.editing_index is None:
            messagebox.showerror("Erro", "Nenhuma árvore selecionada para editar.")
            return
        try:
            number = int(self.number_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Número inválido.")
            return
        for idx, tree in enumerate(self.trees):
            if idx != self.editing_index and tree["number"] == number:
                messagebox.showerror("Erro", "Já existe uma árvore com esse número.")
                return
        name = self.name_entry.get().strip()
        hints = [self.hints_listbox.get(i) for i in range(self.hints_listbox.size())]
        comments = [self.comments_listbox.get(i) for i in range(self.comments_listbox.size())]
        try:
            lat = float(self.lat_entry.get().strip())
            lng = float(self.lng_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Coordenadas inválidas.")
            return
        tree = {
            "number": number,
            "name": name,
            "hints": hints,
            "comments": comments,
            "coordinates": {"lat": lat, "lng": lng}
        }
        self.trees[self.editing_index] = tree
        save_trees(self.trees)
        messagebox.showinfo("Sucesso", "Árvore editada com sucesso!")
        self.clear_fields()
        self.editing_index = None
        self.refresh_trees_listbox()

    def remove_selected_tree(self):
        selection = self.trees_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma árvore para remover.")
            return
        idx = self.filtered_indices[selection[0]]
        tree = self.trees[idx]
        if messagebox.askyesno("Remover", f"Remover árvore '{tree.get('name','')}' (número {tree.get('number','')})?"):
            del self.trees[idx]
            save_trees(self.trees)
            self.refresh_trees_listbox()
            self.clear_fields()
            self.editing_index = None

    def edit_selected_tree(self):
        selection = self.trees_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma árvore para editar.")
            return
        idx = self.filtered_indices[selection[0]]
        tree = self.trees[idx]
        self.editing_index = idx
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, str(tree.get("number", "")))
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, tree.get("name", ""))
        self.hints_listbox.delete(0, tk.END)
        for hint in tree.get("hints", []):
            self.hints_listbox.insert(tk.END, hint)
        self.hint_entry.delete(0, tk.END)
        self.comments_listbox.delete(0, tk.END)
        for comment in tree.get("comments", []):
            self.comments_listbox.insert(tk.END, comment)
        self.comment_entry.delete(0, tk.END)
        coords = tree.get("coordinates", {})
        self.lat_entry.delete(0, tk.END)
        self.lat_entry.insert(0, str(coords.get("lat", "")))
        self.lng_entry.delete(0, tk.END)
        self.lng_entry.insert(0, str(coords.get("lng", "")))

    def on_tree_select(self, event):
        # Optional: auto-load on select
        pass

    def clear_fields(self):
        self.number_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.hints_listbox.delete(0, tk.END)
        self.hint_entry.delete(0, tk.END)
        self.comments_listbox.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)
        self.lat_entry.delete(0, tk.END)
        self.lng_entry.delete(0, tk.END)
        self.editing_index = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeAdminApp(root)
    root.mainloop()
