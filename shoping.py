# Ziel: Aufgabenstellung für ein Python-Programm: "Einkaufslisten-Manager"
# Zeitlimit, heute der 07.10 bis 15:00 Uhr

# Erstellen Sie ein einfaches Desktop-Anwendungsprogramm in Python, das Benutzern hilft, Einkaufslisten zu verwalten. Das Programm verwendet Tkinter für
# die Benutzeroberfläche, PIL (Pillow) für die Bildverarbeitung und speichert die Einkaufslisten in einer externen .txt-Datei.

# Themenbeschreibung
# Das Programm ermöglicht es Benutzern, Artikel zu ihrer Einkaufsliste hinzuzufügen, anzuzeigen und zu entfernen. Benutzer können auch ein Bild des
# gewünschten Artikels hochladen, um eine visuelle Referenz zu haben.

# Anforderungen ---  Benutzeroberfläche:

# Erstellen Sie ein Fenster mit Tkinter, das folgende Komponenten enthält:
# Ein Eingabefeld für den Artikelname.
# Ein Button, um den Artikel zur Einkaufsliste hinzuzufügen.
# Ein Button, um den Artikel aus der Liste zu entfernen.
# Ein Button, um die gesamte Einkaufsliste anzuzeigen.
# Ein Label zur Anzeige der aktuellen Einkaufslisteninhalte.

# Bildverarbeitung:
# Ermöglichen Sie es dem Benutzer, ein Bild des Artikels auszuwählen (z.B. durch Drag & Drop oder einen Datei-Dialog) und zeigen Sie dieses Bild in der
# Anwendung an.
# Das Bild sollte in der Benutzeroberfläche dargestellt werden.

# Speichern und Laden von Einkaufsdaten:
# Wenn der Benutzer einen Artikel hinzufügt, sollen die Artikel in einer .txt-Datei gespeichert werden.
# Beim Start des Programms sollen die Artikel aus der .txt-Datei geladen und in der Liste angezeigt werden.

# Zusätzliche Funktionen:
# Implementieren Sie eine Funktion, um die Liste der Artikel zu aktualisieren, wenn ein neuer Artikel hinzugefügt oder entfernt wird.
# Stellen Sie sicher, dass die Anwendung keine doppelten Artikel speichert.

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os


class EinkaufslisteApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Einkaufsliste")

		self.frame = tk.Frame(self.root)
		self.frame.pack(pady=20)

		self.item_entry = tk.Entry(self.frame, width=50)
		self.item_entry.grid(row=0, column=0, padx=10)

		self.add_button = tk.Button(self.frame, text="Hinzufügen", command=self.hinzufügen)
		self.add_button.grid(row=0, column=1)

		self.listbox = tk.Listbox(self.root, width=80, height=20, selectmode=tk.SINGLE)
		self.listbox.pack(pady=20)
		self.listbox.bind("<<ListboxSelect>>", self.display_image)

		self.image_frame = tk.Frame(self.root)
		self.image_frame.pack(pady=10)

		self.logo_img = Image.open("einkaufsliste_logo.png")
		self.logo_img = self.logo_img.resize((100, 100), Image.LANCZOS)
		self.logo_photo = ImageTk.PhotoImage(self.logo_img)
		self.logo_label = tk.Label(self.image_frame, image=self.logo_photo)
		self.logo_label.pack()

		self.button_frame = tk.Frame(self.root)
		self.button_frame.pack(pady=10)

		self.delete_button = tk.Button(self.button_frame, text="Ausgewähltes löschen", command=self.löschen)
		self.delete_button.grid(row=0, column=0, padx=10)

		self.delete_all_button = tk.Button(self.button_frame, text="Alle löschen", command=self.alle_löschen)
		self.delete_all_button.grid(row=0, column=1, padx=10)

		self.done_button = tk.Button(self.button_frame, text="Als erledigt markieren",
									 command=self.als_erledigt_markieren)
		self.done_button.grid(row=0, column=2, padx=10)

		self.save_button = tk.Button(self.button_frame, text="Speichern", command=self.speichern)
		self.save_button.grid(row=0, column=3, padx=10)

		self.load_button = tk.Button(self.button_frame, text="Laden", command=self.laden)
		self.load_button.grid(row=0, column=4, padx=10)

		self.add_image_button = tk.Button(self.button_frame, text="Bild hinzufügen", command=self.bild_hinzufügen)
		self.add_image_button.grid(row=0, column=5, padx=10)

		self.images = {}

	def hinzufügen(self):
		item = self.item_entry.get()
		if item:
			self.listbox.insert(tk.END, item)
			self.item_entry.delete(0, tk.END)
		else:
			messagebox.showwarning("Warnung", "Bitte geben Sie einen Artikel ein!")

	def löschen(self):
		selected_item_index = self.listbox.curselection()
		if selected_item_index:
			item_text = self.listbox.get(selected_item_index)
			del self.images[item_text]
			self.listbox.delete(selected_item_index)
			self.logo_label.config(image=self.logo_photo)
		else:
			messagebox.showwarning("Warnung", "Bitte wählen Sie einen Artikel aus!")

	def alle_löschen(self):
		self.listbox.delete(0, tk.END)
		self.images.clear()
		self.logo_label.config(image=self.logo_photo)

	def als_erledigt_markieren(self):
		selected_item_index = self.listbox.curselection()
		if selected_item_index:
			item_text = self.listbox.get(selected_item_index)
			self.listbox.delete(selected_item_index)
			self.listbox.insert(selected_item_index, f"{item_text} - Erledigt")
		else:
			messagebox.showwarning("Warnung", "Bitte wählen Sie einen Artikel aus!")

	def speichern(self):
		file_path = filedialog.asksaveasfilename(defaultextension=".txt",
												 filetypes=[("Text dateien", "*.txt"), ("Alle dateien", "*.*")])
		if file_path:
			with open(file_path, 'w') as file:
				for item in self.listbox.get(0, tk.END):
					file.write(f"{item}\n")
					img_path = self.images.get(item.replace(" - Erledigt", ""), "")
					if img_path:
						file.write(f"IMG:{img_path}\n")
			messagebox.showinfo("Info", "Einkaufsliste gespeichert!")

	def laden(self):
		file_path = filedialog.askopenfilename(defaultextension=".txt",
											   filetypes=[("Text dateien", "*.txt"), ("Alle dateien", "*.*")])
		if file_path:
			self.listbox.delete(0, tk.END)
			self.images.clear()
			with open(file_path, 'r') as file:
				for line in file:
					line = line.strip()
					if line.startswith("IMG:"):
						img_path = line.replace("IMG:", "")
						self.images[last_item] = img_path
					else:
						self.listbox.insert(tk.END, line)
						last_item = line
			messagebox.showinfo("Info", "Einkaufsliste geladen!")

	def bild_hinzufügen(self):
		selected_item_index = self.listbox.curselection()
		if not selected_item_index:
			messagebox.showwarning("Warnung", "Bitte wählen Sie einen Artikel aus!")
			return

		item_text = self.listbox.get(selected_item_index).replace(" - Erledigt", "")
		img_path = filedialog.askopenfilename(filetypes=[("Bilddateien", "*.jpg;*.png;*.gif"), ("Alle dateien", "*.*")])
		if img_path:
			self.images[item_text] = img_path
			self.display_image()

	def display_image(self, event=None):
		selected_item_index = self.listbox.curselection()
		if selected_item_index:
			item_text = self.listbox.get(selected_item_index).replace(" - Erledigt", "")
			img_path = self.images.get(item_text)
			if img_path and os.path.exists(img_path):
				img = Image.open(img_path)
				img = img.resize((100, 100), Image.LANCZOS)
				self.current_photo = ImageTk.PhotoImage(img)
				self.logo_label.config(image=self.current_photo)
			else:
				self.logo_label.config(image=self.logo_photo)
		else:
			self.logo_label.config(image=self.logo_photo)


if __name__ == "__main__":
	root = tk.Tk()
	app = EinkaufslisteApp(root)
	root.mainloop()

