import random
import statistics

NUM_PAID_SPINS = 10000000
BET_PER_LINE = 1
NUM_LINES = 10
BET_PER_SPIN = BET_PER_LINE * NUM_LINES

ROWS = 3
REELS = 5


PAYTABLE = {
    "Wild": {3: 100, 4: 200, 5: 400},
    "2": {3: 80, 4: 150, 5: 300},
    "3": {3: 50, 4: 100, 5: 200},
    "4": {3: 40, 4: 80, 5: 150},
    "6": {3: 30, 4: 40, 5: 60},
    "7": {3: 20, 4: 30, 5: 40},
    "8": {3: 10, 4: 15, 5: 30},
    "9": {3: 5, 4: 10, 5: 15},
}


# Normal reel distribution per reel
NORMAL_DISTRIBUTIONS = [
    {
        "Wild": 0,
        "Scatter": 1,
        "2": 5,
        "3": 5,
        "4": 5,
        "6": 4,
        "7": 10,
        "8": 10,
        "9": 10,
    },  # Reel 1
    {
        "Wild": 2,
        "Scatter": 2,
        "2": 5,
        "3": 5,
        "4": 5,
        "6": 5,
        "7": 8,
        "8": 10,
        "9": 10,
    },  # Reel 2
    {
        "Wild": 1,
        "Scatter": 2,
        "2": 5,
        "3": 5,
        "4": 5,
        "6": 8,
        "7": 8,
        "8": 8,
        "9": 8,
    },  # Reel 3
    {
        "Wild": 1,
        "Scatter": 1,
        "2": 5,
        "3": 5,
        "4": 5,
        "6": 8,
        "7": 9,
        "8": 8,
        "9": 8,
    },  # Reel 4
    {
        "Wild": 2,
        "Scatter": 2,
        "2": 7,
        "3": 6,
        "4": 6,
        "6": 10,
        "7": 10,
        "8": 12,
        "9": 11,
    },  # Reel 5
]
# Free-spin reel distribution per reel
FS_DISTRIBUTIONS = [
    {  # Reel 1
        "Wild": 4,
        "2": 3,
        "3": 3,
        "4": 3,
        "6": 9,
        "7": 9,
        "8": 10,
        "9": 9,
    },
    {  # Reel 2
        "Wild": 5,
        "2": 3,
        "3": 3,
        "4": 2,
        "6": 8,
        "7": 9,
        "8": 10,
        "9": 10,
    },
    {  # Reel 3
        "Wild": 6,
        "2": 2,
        "3": 3,
        "4": 3,
        "6": 8,
        "7": 8,
        "8": 10,
        "9": 10,
    },
    {  # Reel 4
        "Wild": 5,
        "2": 3,
        "3": 2,
        "4": 3,
        "6": 9,
        "7": 8,
        "8": 10,
        "9": 10,
    },
    {  # Reel 5
        "Wild": 4,
        "2": 3,
        "3": 3,
        "4": 3,
        "6": 9,
        "7": 9,
        "8": 9,
        "9": 10,
    },
]
# 10 paylines using row index: 0=top, 1=middle, 2=bottom
PAYLINES = [
    [1, 1, 1, 1, 1],  # middle
    [0, 0, 0, 0, 0],  # top
    [2, 2, 2, 2, 2],  # bottom
    [0, 1, 2, 1, 0],  # V
    [2, 1, 0, 1, 2],  # inverted V
    [2, 2, 1, 0, 0],  # up slope
    [0, 0, 1, 2, 2],  # down slope
    [0, 1, 1, 1, 2],  # top to bottom
    [2, 1, 1, 1, 0],  # bottom to top
    [0, 2, 0, 2, 0],  # zigzag
]


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------


def build_reel(distribution):
    reel = []
    for symbol, count in distribution.items():
        reel.extend([symbol] * count)
    random.shuffle(reel)
    return reel


def build_reels(distributions):
    return [build_reel(distribution) for distribution in distributions]


NORMAL_REELS = build_reels(NORMAL_DISTRIBUTIONS)

FS_REELS = build_reels(FS_DISTRIBUTIONS)


def spin_grid(reels):
    grid = []

    for reel in reels:
        stop = random.randint(0, len(reel) - 1)

        top = reel[(stop - 1) % len(reel)]
        middle = reel[stop]
        bottom = reel[(stop + 1) % len(reel)]

        grid.append([top, middle, bottom])

    return grid


def count_scatters(grid):
    return sum(1 for reel in grid for symbol in reel if symbol == "Scatter")


def free_spins_awarded(scatter_count):
    if scatter_count == 3:
        return 10
    elif scatter_count == 4:
        return 15
    elif scatter_count >= 5:
        return 20
    return 0


def get_winning_symbol(symbols):
    for symbol in symbols:
        if symbol != "Wild" and symbol != "Scatter":
            return symbol

    if all(symbol == "Wild" for symbol in symbols):
        return "Wild"

    return None


def evaluate_line(symbols):
    winning_symbol = get_winning_symbol(symbols)

    if winning_symbol is None:
        return 0

    match_count = 0

    for symbol in symbols:
        if symbol == winning_symbol or symbol == "Wild":
            match_count += 1
        else:
            break

    if match_count >= 3:
        return PAYTABLE.get(winning_symbol, {}).get(match_count, 0) * BET_PER_LINE

    return 0


def evaluate_grid(grid):
    total_win = 0

    for line in PAYLINES:
        symbols = []

        for reel_index, row_index in enumerate(line):
            symbols.append(grid[reel_index][row_index])

        total_win += evaluate_line(symbols)

    return total_win


# -----------------------------
# SIMULATION
# -----------------------------


def run_simulation(num_paid_spins=10000000):
    total_bet = 0
    total_win = 0

    base_win = 0
    free_spin_win = 0

    paid_spins_done = 0
    actual_spins = 0
    free_spins_remaining = 0
    bonus_triggers = 0
    hit_count = 0

    spin_wins = []

    while paid_spins_done < num_paid_spins or free_spins_remaining > 0:

        if free_spins_remaining > 0:
            mode = "Free Spin"
            reels = FS_REELS
            bet = 0
            free_spins_remaining -= 1
        else:
            mode = "Normal"
            reels = NORMAL_REELS
            bet = BET_PER_SPIN
            paid_spins_done += 1
            total_bet += bet

        grid = spin_grid(reels)
        win = evaluate_grid(grid)

        if mode == "Normal":
            scatter_count = count_scatters(grid)
            fs_awarded = free_spins_awarded(scatter_count)

            if fs_awarded > 0:
                bonus_triggers += 1
                free_spins_remaining += fs_awarded
        else:
            fs_awarded = 0

        total_win += win
        spin_wins.append(win)

        if win > 0:
            hit_count += 1

        if mode == "Normal":
            base_win += win
        else:
            free_spin_win += win

        actual_spins += 1

    rtp = total_win / total_bet
    base_rtp = base_win / total_bet
    fs_rtp = free_spin_win / total_bet
    hit_frequency = hit_count / actual_spins
    bonus_frequency = bonus_triggers / num_paid_spins
    avg_win = statistics.mean(spin_wins)
    std_dev = statistics.pstdev(spin_wins)

    print("Simulation Completed")
    print("-----------------------------")
    print(f"Paid Spins: {num_paid_spins}")
    print(f"Actual Spins Including Free Spins: {actual_spins}")
    print(f"Total Bet: {total_bet}")
    print(f"Total Win: {total_win}")
    print(f"Final RTP: {rtp:.2%}")
    print(f"Base Game RTP: {base_rtp:.2%}")
    print(f"Free Spin RTP: {fs_rtp:.2%}")
    print(f"Hit Frequency: {hit_frequency:.2%}")
    print(f"Bonus Triggers: {bonus_triggers}")
    print(
        f"Bonus Frequency: 1 in {num_paid_spins / bonus_triggers:.2f} spins"
        if bonus_triggers > 0
        else "No bonus triggered"
    )
    print(f"Average Win: {avg_win:.4f}")
    print(f"Standard Deviation: {std_dev:.4f}")

    return {
        "RTP": rtp,
        "Base RTP": base_rtp,
        "Free Spin RTP": fs_rtp,
        "Hit Frequency": hit_frequency,
        "Bonus Frequency": bonus_frequency,
        "Bonus Triggers": bonus_triggers,
        "Total Bet": total_bet,
        "Total Win": total_win,
        "Standard Deviation": std_dev,
    }


# Run 100k paid spins
results = run_simulation(NUM_PAID_SPINS)
