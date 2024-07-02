import random
import os
from playsound import playsound  # type: ignore

class SlotMachine:
    MAX_LINES = 4
    MAX_BET = 10000
    MIN_BET = 10
    ROWS = 4
    COLS = 3

    symbol_count = {
        "£": 6,
        "$": 6,
        "Ħ": 8
    }

    symbol_values = {
        "£": 8,
        "$": 5,
        "Ħ": 3
    }

    def __init__(self, balance):
        self.balance = balance

    def deposit(self):
        while True:
            amount = input("Enter the amount you would like to add: ")
            if amount.isdigit() and int(amount) > 0:
                self.balance += int(amount)
                break
            else:
                print("Amount must be a positive number.")
    
    def get_number_of_lines(self):
        while True:
            lines = input(f"Enter the number of lines to bet on (1 - {self.MAX_LINES}): ")
            if lines.isdigit() and 1 <= int(lines) <= self.MAX_LINES:
                return int(lines)
            else:
                print("Please enter a valid number of lines.")
    
    def get_bet(self):
        while True:
            amount = input(f"Enter the amount you would like to bet on each line ({self.MIN_BET} - {self.MAX_BET}): ")
            if amount.isdigit() and self.MIN_BET <= int(amount) <= self.MAX_BET:
                return int(amount)
            else:
                print(f"Please enter a bet amount between {self.MIN_BET} and {self.MAX_BET}.")

    def get_slot_machine_spin(self):
        all_symbols = []
        for symbol, count in self.symbol_count.items():
            all_symbols.extend([symbol] * count)

        columns = []
        for _ in range(self.COLS):
            column = random.sample(all_symbols, self.ROWS)
            columns.append(column)

        return columns
    
    def print_slot_machine(self, columns):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                print(columns[col][row], end=" | " if col < self.COLS - 1 else " ")
            print()
    
    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []

        for line in range(lines):
            symbols_in_line = [columns[col][line] for col in range(self.COLS)]
            if all(symbol == symbols_in_line[0] for symbol in symbols_in_line):
                symbol = symbols_in_line[0]
                winnings += bet * self.symbol_values[symbol]
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def play_spin_sound(self):
        try:
            playsound('spin_sound.mp3')
        except Exception as e:
            print(f"Error playing spin sound: {e}")

    def play_win_sound(self):
        try:
            playsound('win_sound.mp3')
        except Exception as e:
            print(f"Error playing win sound: {e}")

    def play_loss_sound(self):
        try:
            playsound('loss_sound.mp3')
        except Exception as e:
            print(f"Error playing loss sound: {e}")

    def spin(self):
        lines = self.get_number_of_lines()
        while True:
            bet = self.get_bet()
            total_bet = lines * bet

            if total_bet > self.balance:
                print(f"Sorry, you don't have enough balance to bet. Your current balance is {self.balance}")
            else:
                break

        print(f"You are betting {bet} on {lines} line(s). Total bet is: {total_bet}")

        self.play_spin_sound()  # Play spin sound

        slots = self.get_slot_machine_spin()
        self.print_slot_machine(slots)

        winnings, winning_lines = self.check_winnings(slots, lines, bet)

        if winnings == 0:
            print("You lost this round.")
            self.play_loss_sound()  # Play loss sound
        else:
            print(f"You win {winnings}")
            self.play_win_sound()  # Play win sound
            if winning_lines:
                print(f"You won on line(s):", *winning_lines)

        self.balance += winnings - total_bet
        print("-----------------------------------------------------------")
        return self.balance

    def save_high_score(self):
        if not os.path.exists('leaderboard.txt'):
            with open('leaderboard.txt', 'w') as file:
                file.write('0\n')

        with open('leaderboard.txt', 'r') as file:
            high_score = int(file.readline().strip())

        if self.balance > high_score:
            with open('leaderboard.txt', 'w') as file:
                file.write(str(self.balance))
            print(f"New high score: {self.balance}")
        else:
            print(f"Your final balance: {self.balance}. High score remains: {high_score}")

    def play(self):
        self.deposit()
        while True:
            print(f"Current balance: {self.balance}")
            answer = input("Press Enter to Spin or Q to Quit the game: ").strip().lower()
            if answer == "q":
                break
            self.balance = self.spin()
        self.save_high_score()
        print(f"You left with {self.balance}")

if __name__ == "__main__":
    initial_balance = 0
    slot_machine = SlotMachine(initial_balance)
    slot_machine.play()
