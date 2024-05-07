import subprocess

def run_game():
    try:
        input()
        subprocess.run(['python', 'C:\Users\Asus\Desktop\networkingFinalProject\Network-Game-Tutorial-master_original\server.py'], check=True)
        input()
        subprocess.run(['python', 'C:\Users\Asus\Desktop\networkingFinalProject\Network-Game-Tutorial-master_original\game.py'], check=True)
        input()
        subprocess.run(['python', 'C:\Users\Asus\Desktop\networkingFinalProject\Network-Game-Tutorial-master_original\game.py'], check=True)
        input()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the game: {e}")
        input()

if __name__ == '__main__':
    run_game()