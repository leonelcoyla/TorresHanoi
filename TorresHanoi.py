import tkinter as tk
from PIL import ImageTk
from PIL import Image

class torresHanoi:
    def __init__(self, root, contenido):
        self.root = root
        self.contenido = contenido

        # Limpiar el frame 
        for widget in self.contenido.winfo_children():
            widget.destroy()

        self.nDiscos = 3 #Inicia con 3 discos
        self.torres = [list(reversed(range(1, self.nDiscos+1))), [], []]

        self.canvas = tk.Canvas(self.contenido, width=950, height=300, bg="White Smoke") #area de dibujo
        self.canvas.pack(pady=40,anchor = "center")

       
        # Frame para número de discos (antes que origen/destino) 
        self.frameDiscos = tk.Frame(self.contenido, bg="White Smoke")
        self.frameDiscos.pack(pady=10)

        tk.Button(self.frameDiscos, text="Ingresar número de discos",
                  bg="White Smoke", command=self.entrarDiscos).pack(side="left", padx=5)
        self.entryDiscos = None  # Se crea al presionar el botón

        # Botones de movimiento (origen, destino, mover) 
        self.botones = tk.Frame(self.contenido, bg="White Smoke")
        self.botones.pack(pady=10)

        self.origenVar = tk.StringVar()
        self.destinoVar = tk.StringVar()

        tk.Label(self.botones, text="Origen:", bg="White Smoke").grid(row=0, column=0)
        tk.Entry(self.botones, textvariable=self.origenVar, width=8, justify='right',
                 font=('Arial', 14, 'bold')).grid(row=0, column=1, padx=5)

        tk.Label(self.botones, text="Destino:", bg="White Smoke").grid(row=0, column=2)
        tk.Entry(self.botones, textvariable=self.destinoVar, width=8, justify='right',
                 font=('Arial', 14, 'bold')).grid(row=0, column=3, padx=5)

        tk.Button(self.botones, text="Mover", bg="White Smoke",
                  width=8, command=self.mover).grid(row=0, column=4, padx=10)

        self.mensaje_label = tk.Label(self.contenido, text="", bg="White Smoke",
                                      fg="red", font=("Arial", 12))
        self.mensaje_label.pack(pady=5)

        self.dibujarTorres()

    def entrarDiscos(self):
        # Evitar múltiples entradas y botones
        for widget in self.frameDiscos.winfo_children():
            if type(widget) in [tk.Entry, tk.Button]:
                if isinstance(widget, tk.Entry) or widget.cget("text") == "Aceptar":
                    widget.destroy()

        self.entryDiscos = tk.Entry(self.frameDiscos, width=8, justify='right', font=('Arial', 14, 'bold'))
        self.entryDiscos.pack(side="left", padx=5)

        tk.Button(self.frameDiscos, text="Aceptar", bg="White Smoke",
                  width=8,command=self.aceptarDiscos).pack(side="left", padx=5)

    def aceptarDiscos(self):
        try:
            n = int(self.entryDiscos.get())
            if n < 1 or n > 8:
                raise ValueError("El número debe estar entre 1 y 8")

            self.nDiscos = n
            self.torres = [list(reversed(range(1, n + 1))), [], []]
            self.dibujarTorres()
            self.mostrarMensaje(f"¡Vamos a jugar! con {n} discos.", "green")
        except ValueError:
            self.mostrarMensaje("Ingrese un número válido entre 1 y 8 discos.")

    def dibujarTorres(self):
        self.canvas.delete("all")

        alturaDisco = 18
        distanciaEntreTorres = [200, 500, 800]
        self.colores = ["yellow", "red", "orange", "cyan", "blue", "Green Yellow", "magenta","Lime"]

        for t, torre in enumerate(self.torres):
            x = distanciaEntreTorres[t]
            self.canvas.create_rectangle(x - 5, 50, x + 5, 220, fill="peru")
            y = 220
            for disco in torre:
                anchoDisco = disco * 18
                color = self.colores[(disco-1)%len(self.colores)]
                self.canvas.create_rectangle(x - anchoDisco, y - alturaDisco, x + anchoDisco, y,
                                             fill=color,outline="black")
                y = y - alturaDisco
            self.canvas.create_text(x, 240, text=str(t + 1), font=("Helvetica", 14,"bold"), fill="blue")

    def algoritmoHanoi(self, n, origen, destino, temporal):
        if n == 1:
            self.moverDisco(origen, destino)
        else:
            self.algoritmoHanoi(n - 1, origen, temporal, destino) #Algoritmo recursivo torres de Hanoi
            self.moverDisco(origen, destino)
            self.algoritmoHanoi(n - 1, temporal, destino, origen)#Algoritmo  recursivo torres de Hanoi

    def moverDisco(self, origen, destino):
        if self.torres[origen]:
            disco = self.torres[origen][-1]
            if not self.torres[destino] or self.torres[destino][-1] > disco:
                self.torres[origen].pop()
                self.torres[destino].append(disco)
                self.dibujarTorres()
                if len(self.torres[2]) == self.nDiscos:
                    self.mostrarMensaje("¡Felicitaciones! terminaste", "blue")
            else:
                self.mostrarMensaje("Movimiento no permitido:  No puede estar un disco grande sobre uno más pequeño.")
        else:
            self.mostrarMensaje("Movimiento incorrecto: Torre de origen vacía.")


    def mover(self):
        self.mostrarMensaje("")  # Limpiar mensaje anterior
        try:
            origen = int(self.origenVar.get()) - 1
            destino = int(self.destinoVar.get()) - 1
            if origen not in [0, 1, 2] or destino not in [0, 1, 2]:
                raise ValueError
            self.moverDisco(origen, destino)
        except ValueError:
            self.mostrarMensaje("Ingrese números válidos (1, 2 o 3).")


    def mostrarMensaje(self, texto, color="red"):
        self.mensaje_label.config(
            text=texto,
            fg=color,
            font=("Comic Sans MS", 12, "bold")
        )



# Aplicación principal con menú
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi")
        self.root.geometry("1200x700")

        self.barra_menu = tk.Menu(self.root)
        self.root.config(menu=self.barra_menu)

        self.barra_menu.add_command(label="Presentación", command=self.presentacion)
        self.barra_menu.add_command(label="Torres de Hanoi", command=self.torresHanoi)
        self.barra_menu.add_command(label="Ayuda", command=self.ayuda)
        self.barra_menu.add_command(label="Acerca de ", command=self.acercade)

        # Frame central 
        self.contenido = tk.Frame(self.root, bg="White Smoke")
        self.contenido.pack(fill="both", expand=True)

    def limpiarFrame():
        for widget in contenido.winfo_children():
            widget.destroy()

    def presentacion(self):
                
        for widget in self.contenido.winfo_children():
                widget.destroy()

        tk.Label(self.contenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="White Smoke").pack() 
        tk.Label(self.contenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="White Smoke").pack() 
        tk.Label(self.contenido, text="BIENVENIDOS A LA APLICACIÓN",
                 font=("Comic Sans MS", 18, "bold"),  fg="#00008B", bg="White Smoke").pack()
        tk.Label(self.contenido, text="LAS TORRES DE HANOI",
                 font=("Arial", 14, "bold"), fg="#00008B", bg="White Smoke").pack()
        tk.Label(self.contenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="White Smoke").pack()
        tk.Label(self.contenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="White Smoke").pack()

        try:
            image = Image.open("TorresHanoi.png")  
            image = image.resize((500,350))
            image_tk = ImageTk.PhotoImage(image)
            imageLabel = tk.Label(self.contenido, image=image_tk, bg="White Smoke")
            imageLabel.image = image_tk
            imageLabel.pack(pady=20)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        tk.Label(self.contenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="White Smoke").pack()
        tk.Label(self.contenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="White Smoke").pack()
        tk.Label(self.contenido, text="TorresHanoi v1.0", font=("Comic Sans MS", 20, "bold"),
                 fg="#00008B", bg="White Smoke").pack()

    def torresHanoi(self):
        torresHanoi(self.root, self.contenido)

    def ayuda(self):
        
        for widget in self.contenido.winfo_children():
                widget.destroy()
            
        tk.Label(self.contenido, text="\n\nINSTRUCCIONES DE USO", bg="White Smoke",
                 font=("Lucida Handwriting", 14,"bold"), fg="#00008B").pack(pady=20)
        tk.Label(self.contenido, text="TorresHanoi v1.0:\n\n", bg="White Smoke",
                 font=("Comic Sans MS", 14,"bold"), fg="#00008B").pack(pady=20)
        tk.Label(self.contenido, text="\n1. Hacer un click en el menu Torres de Hanoi"
                 f"\n2. Hacer un click en el boton ingresar número de discos y luego Aceptar\n"
                 f"2. Para mover los discos de la torre 1 a la torre 3 utilizando como auxiliar la torre, 2\n"
                 f" escribir el número de torre en el origen y escriba el número de torre en el destino'"
                 f"\n 3. y observará el desplazamiento de disco"
                 f"\n 4. Además, considere que un disco grande no puede estar sobre un disco pequeño",
                 bg="White Smoke",
                 font=("Verdana", 14)).pack(pady=20)

    def acercade(self):
            for widget in self.contenido.winfo_children():
                widget.destroy()

            
            frameTextos = tk.Frame(self.contenido, bg="White Smoke")
            frameTextos.pack(pady=20)

            # Título
            tk.Label(frameTextos, text="\n\n\n\nJuego de las Torres de Hanoi\nTorresHanoi v1.0",
                     bg="White Smoke", font=("Comic Sans MS", 14, "bold"),
                     fg="#00008B").pack(pady=(0, 10))

            # Lista de autores
            autores = [
                            "\nDesarrollado por: Leonel Coyla Idme",
                            "Elqui Yeye Pari Condori",
                            "Juan Reynaldo Paredes Quispe",
                            "José Pánfilo Tito Lipa",
                            "Alfredo Mamani Canqui",
            ]

            # Etiqueta por autor
            for autor in autores:
                tk.Label(frameTextos, text=autor, bg="White Smoke",
                         font=("Comic Sans MS", 14)).pack(pady=2)

            labelAcercade = tk.Label(self.contenido, text= "\n\nLanzamiento : 12 de mayo  2025",
                                      font=("Comic Sans MS", 14),fg="#003366",bg="White Smoke")
            labelAcercade.pack(pady=(1,10))
            labelAcercade = tk.Label(self.contenido, text= "Contacto: lcoyla@unap.edu.pe",
                                      font=("Comic Sans MSl", 14),fg="#003366",bg="White Smoke")
            labelAcercade.pack(pady=(1,10))


# Ejecutar aplicación
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
if __name__ == "__main__":
    main()
