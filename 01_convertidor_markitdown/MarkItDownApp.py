import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from markitdown import MarkItDown


class MarkItDownApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor MarkItDown")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        # Inicializar el convertidor de MarkItDown
        self.md = MarkItDown()

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = ttk.Label(
            self.root,
            text="Convertir archivos a Markdown",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=20)

        # Instrucciones
        instructions = ttk.Label(
            self.root,
            text="Selecciona uno o varios archivos (PDF, Word, Excel, etc.)\n"
            "La versión en Markdown se guardará en la misma carpeta.",
            justify="center",
        )
        instructions.pack(pady=10)

        # Botón de selección
        self.btn_select = ttk.Button(
            self.root, text="Seleccionar Archivos", command=self.select_and_convert
        )
        self.btn_select.pack(pady=20, ipadx=10, ipady=5)

        # Barra de estado
        self.status_label = ttk.Label(
            self.root, text="Listo", foreground="gray"
        )
        self.status_label.pack(side="bottom", pady=10)

    def select_and_convert(self):
        # Deshabilitar botón durante el proceso
        self.btn_select.config(state="disabled")
        self.status_label.config(
            text="Seleccionando archivos...", foreground="blue"
        )

        # Abrir el selector de archivos (permite múltiple selección)
        files = filedialog.askopenfilenames(
            title="Selecciona archivos para convertir",
            filetypes=[
                (
                    "Archivos soportados",
                    "*.docx *.xlsx *.pptx *.pdf *.txt *.html",
                ),
                ("Todos los archivos", "*.*"),
            ],
        )

        if not files:
            self.status_label.config(text="Operación cancelada", foreground="red")
            self.btn_select.config(state="normal")
            return

        exitosos = 0
        errores = 0

        for file_path in files:
            try:
                self.status_label.config(
                    text=f"Convirtiendo: {os.path.basename(file_path)}...",
                    foreground="orange",
                )
                self.root.update()

                # Separar la ruta y la extensión original
                base_path, _ = os.path.splitext(file_path)
                # Crear la nueva ruta con extensión .md en la misma carpeta
                output_path = f"{base_path}.md"

                # Ejecutar la conversión con MarkItDown
                result = self.md.convert(file_path)

                # Guardar el resultado en el archivo .md
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.text_content)

                exitosos += 1
            except Exception as e:
                print(f"Error al convertir {file_path}: {e}")
                errores += 1

        # Finalización
        self.btn_select.config(state="normal")
        self.status_label.config(text="Proceso finalizado", foreground="green")

        # Mostrar mensaje de éxito o advertencia
        if errores == 0:
            messagebox.showinfo(
                "Éxito",
                f"¡Conversión completada!\nSe convirtieron {exitosos} archivo(s) correctamente.",
            )
        else:
            messagebox.showwarning(
                "Completado con errores",
                f"Proceso terminado.\nExitosos: {exitosos}\nErrores: {errores}",
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkItDownApp(root)
    root.mainloop()
