wins = 0
losses = 0
attempts_left = 5

def init_attempts():
    global attempts_left
    attempts_left = 5

def record_failed_attempt():
    global attempts_left
    attempts_left -= 1

def record_win():
    global wins
    wins += 1

def record_loss():
    global losses
    losses += 1

def show_score():
    print(f"Wins: {wins}, Losses: {losses}")
