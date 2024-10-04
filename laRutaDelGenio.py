import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

# Variables temporales para almacenar el estado del juego
user_data = {
    "user": "",
    "total_score": 0,
    "games_played": 0,
    "level": 1,
    "achievements": []
}

# Sistema de logros basado en niveles
def check_achievements():
    level = user_data["level"]
    achievements = user_data.get("achievements", [])

    # Definición de logros por nivel
    if level >= 1 and "Comienza la aventura (Nivel 1)" not in achievements:
        achievements.append("Comienza la aventura (Nivel 1)")
    if level >= 5 and "Dominio básico (Nivel 5)" not in achievements:
        achievements.append("Dominio básico (Nivel 5)")
    if level >= 10 and "Maestro de mini-juegos (Nivel 10)" not in achievements:
        achievements.append("Maestro de mini-juegos (Nivel 10)")
    if level >= 15 and "Experto en matemáticas (Nivel 15)" not in achievements:
        achievements.append("Experto en matemáticas (Nivel 15)")

    user_data["achievements"] = achievements


# Mini-juego 1: Reto de rapidez
def play_speed_challenge():
    start_time = time.time()
    correct_count = 0

    while time.time() - start_time < 30:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        problem = f"{num1} + {num2}"
        correct_answer = num1 + num2

        user_answer = simpledialog.askstring("Reto de Rapidez", f"Resuelve: {problem}")
        if user_answer is not None and user_answer.isdigit() and int(user_answer) == correct_answer:
            correct_count += 1

    messagebox.showinfo("Reto de Rapidez", f"¡Has resuelto {correct_count} problemas en 30 segundos!")
    return correct_count * 10


# Mini-juego 2: Adivina el número
def play_number_guessing():
    secret_number = random.randint(1, 100)
    attempts = 0
    guess = None

    while guess != secret_number:
        guess = simpledialog.askinteger("Adivina el Número", "Adivina un número entre 1 y 100:")
        if guess is None:
            return 0
        attempts += 1
        if guess < secret_number:
            messagebox.showinfo("Adivina el Número", "¡Demasiado bajo!")
        elif guess > secret_number:
            messagebox.showinfo("Adivina el Número", "¡Demasiado alto!")

    messagebox.showinfo("Adivina el Número", f"¡Correcto! Lo adivinaste en {attempts} intentos.")
    return max(100 - attempts * 10, 10)


# Mini-juego 3: Cálculo mental rápido
def play_fast_math():
    score = 0
    for _ in range(5):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operation = random.choice(["+", "-", "*"])
        if operation == "+":
            correct_answer = num1 + num2
        elif operation == "-":
            correct_answer = num1 - num2
        elif operation == "*":
            correct_answer = num1 * num2

        problem = f"{num1} {operation} {num2}"
        start_time = time.time()

        user_answer = simpledialog.askstring("Cálculo Mental", f"Resuelve rápidamente: {problem}")
        if user_answer is not None and user_answer.isdigit() and int(user_answer) == correct_answer:
            if time.time() - start_time <= 5:  # Debe resolverlo en menos de 5 segundos
                score += 20
            else:
                messagebox.showinfo("Cálculo Mental", "¡Respuesta correcta, pero tardaste demasiado!")
        else:
            messagebox.showinfo("Cálculo Mental", f"¡Incorrecto! La respuesta era {correct_answer}")

    messagebox.showinfo("Cálculo Mental", f"Tu puntaje en el Cálculo Mental es: {score}")
    return score


# Jugar un mini-juego al azar
def play_random_mini_game():
    mini_game = random.choice([play_speed_challenge, play_number_guessing, play_fast_math])
    score = mini_game()

    user_data['total_score'] += score
    user_data['games_played'] += 1

    if user_data['games_played'] % 5 == 0:
        user_data['level'] += 1
        messagebox.showinfo("Nivel alcanzado", f"¡Felicidades! Has alcanzado el nivel {user_data['level']}")
        check_achievements()  # Verificar logros al alcanzar un nuevo nivel múltiplo de 5

    update_game_status()


# Actualizar estado del juego en la interfaz
def update_game_status():
    label_status.config(
        text=f"Jugador: {user_data['user']}\nPuntaje total: {user_data['total_score']}\nNivel: {user_data['level']}")


# Mostrar logros
def show_achievements():
    if not user_data['achievements']:
        messagebox.showinfo("Logros", "Aún no has conseguido logros.")
    else:
        achievements_text = "\n".join(user_data['achievements'])
        messagebox.showinfo("Logros", f"Has conseguido los siguientes logros:\n{achievements_text}")


# Menú y botones
def create_menu(root):
    menu_bar = tk.Menu(root)

    # Menú de juego
    game_menu = tk.Menu(menu_bar, tearoff=0)
    game_menu.add_command(label="Jugar", command=play_random_mini_game)
    game_menu.add_separator()
    game_menu.add_command(label="Salir", command=root.quit)

    # Menú de logros
    achievements_menu = tk.Menu(menu_bar, tearoff=0)
    achievements_menu.add_command(label="Mostrar Logros", command=show_achievements)

    menu_bar.add_cascade(label="Juego", menu=game_menu)
    menu_bar.add_cascade(label="Logros", menu=achievements_menu)

    root.config(menu=menu_bar)


# Mostrar instrucciones en la ventana principal
def show_instructions_in_main():
    instructions = """
    ¡Bienvenido a La Ruta Del Genio!

    Juegos disponibles:
    1. Reto de rapidez: Resuelve tantos problemas como puedas en 30 segundos.
    2. Adivina el número: Adivina un número entre 1 y 100 con pistas.
    3. Cálculo mental rápido: Resuelve operaciones matemáticas dentro de un tiempo límite.
    (Los juegos se daran al azar)

    - El nivel aumentara dependiendo de los puntos obtenidos.

    ¡Diviértete, gana puntos y desbloquea logros cada 5 niveles!
    """
    label_instructions.config(text=instructions)


# Crear la interfaz gráfica
def create_gui():
    global label_status, label_instructions

    root = tk.Tk()
    root.title("La Ruta Del Genio")

    # Solicitar nombre de usuario al inicio
    user_data["user"] = simpledialog.askstring("Nombre de Usuario", "Introduce tu nombre de usuario:")

    if not user_data["user"]:
        messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
        return

    # Crear menú
    create_menu(root)

    # Estado del juego
    label_status = tk.Label(root,
                            text=f"Jugador: {user_data['user']}\nPuntaje total: {user_data['total_score']}\nNivel: {user_data['level']}")
    label_status.pack(pady=10)

    # Instrucciones en la ventana principal
    label_instructions = tk.Label(root, text="")
    label_instructions.pack(pady=10)
    show_instructions_in_main()  # Mostrar las instrucciones en la ventana principal

    # Botones
    btn_play = tk.Button(root, text="Jugar", command=play_random_mini_game)
    btn_play.pack(pady=5)

    btn_achievements = tk.Button(root, text="Mostrar Logros", command=show_achievements)
    btn_achievements.pack(pady=5)

    root.mainloop()

# Ejecutar el juego
if __name__ == "__main__":
    create_gui()