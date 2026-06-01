import random
import statistics

# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_SPINS = 1_000_000

BET_PER_LINE = 1
NUM_LINES = 20
BET_PER_SPIN = BET_PER_LINE * NUM_LINES

REELS = 5

# Progressive Jackpot Settings
SEED_JACKPOT = 10_000
JACKPOT_CONTRIBUTION_RATE = 0.01  # 1% of every paid spin
JACKPOT_TRIGGER_PROBABILITY = 1 / 100_000

# Paytable: 3OAK, 4OAK, 5OAK
PAYTABLE = {
    "Wild": {3: 160.5, 4: 401.25, 5: 802.5},
    "Dragon": {3: 128.4, 4: 321, 5: 642},
    "Unicorn": {3: 96.3, 4: 240.75, 5: 481.5},
    "Phoenix": {3: 64.2, 4: 160.5, 5: 321},
    "Wizard": {3: 40.66, 4: 96.3, 5: 192.6},
    "Knight": {3: 32.1, 4: 80.25, 5: 160.5},
    "Gem": {3: 24.61, 4: 48.15, 5: 96.3},
    "Shield": {3: 16.05, 4: 40.66, 5: 80.25},
    "Coin": {3: 12.84, 4: 32.1, 5: 64.2},
}

# RTP adjustment after previous tuning
ADJUSTMENT = 0.976

PAYTABLE = {
    symbol: {kind: payout * ADJUSTMENT for kind, payout in pays.items()}
    for symbol, pays in PAYTABLE.items()
}

# Reel distribution per 50-stop reel
DISTRIBUTION = {
    "Wild": 1,
    "Jackpot": 1,
    "Dragon": 3,
    "Unicorn": 4,
    "Phoenix": 5,
    "Wizard": 6,
    "Knight": 7,
    "Gem": 8,
    "Shield": 7,
    "Coin": 8,
}

# 20 paylines using row index:
# 0 = top, 1 = middle, 2 = bottom
PAYLINES = [
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2],
    [0, 1, 2, 1, 0],
    [2, 1, 0, 1, 2],
    [0, 0, 1, 2, 2],
    [2, 2, 1, 0, 0],
    [0, 1, 1, 1, 2],
    [2, 1, 1, 1, 0],
    [0, 2, 0, 2, 0],
    [1, 0, 0, 0, 1],
    [1, 2, 2, 2, 1],
    [0, 0, 1, 0, 0],
    [2, 2, 1, 2, 2],
    [1, 1, 0, 1, 1],
    [1, 1, 2, 1, 1],
    [0, 1, 0, 1, 0],
    [2, 1, 2, 1, 2],
    [1, 0, 1, 0, 1],
    [1, 2, 1, 2, 1],
]


# -----------------------------
# REEL FUNCTIONS
# -----------------------------


def build_reel(distribution):
    reel = []

    for symbol, count in distribution.items():
        reel.extend([symbol] * count)

    random.shuffle(reel)

    return reel


def build_reels():
    reels = []

    for _ in range(REELS):
        reels.append(build_reel(DISTRIBUTION))

    return reels


REEL_STRIPS = build_reels()


# -----------------------------
# SPIN FUNCTIONS
# -----------------------------


def spin_grid():
    grid = []

    for reel in REEL_STRIPS:
        stop = random.randint(0, len(reel) - 1)

        top = reel[(stop - 1) % len(reel)]
        middle = reel[stop]
        bottom = reel[(stop + 1) % len(reel)]

        grid.append([top, middle, bottom])

    return grid


def get_winning_symbol(symbols):
    for symbol in symbols:
        if symbol != "Wild" and symbol != "Jackpot":
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
        line_symbols = []

        for reel_index, row_index in enumerate(line):
            line_symbols.append(grid[reel_index][row_index])

        total_win += evaluate_line(line_symbols)

    return total_win


def count_jackpot_symbols(grid):
    count = 0

    for reel in grid:
        for symbol in reel:
            if symbol == "Jackpot":
                count += 1

    return count


# -----------------------------
# SIMULATION
# -----------------------------


def run_simulation():
    total_bet = 0
    total_win = 0

    base_game_win = 0
    jackpot_total_paid = 0

    hit_count = 0
    base_hit_count = 0

    jackpot_hits = 0
    visible_jackpot_5plus_count = 0

    jackpot_pool = SEED_JACKPOT

    spin_wins = []

    for spin_number in range(1, NUM_SPINS + 1):
        grid = spin_grid()

        base_win = evaluate_grid(grid)

        jackpot_symbol_count = count_jackpot_symbols(grid)

        if jackpot_symbol_count >= 5:
            visible_jackpot_5plus_count += 1

        # Every paid spin contributes to progressive jackpot pool
        jackpot_pool += BET_PER_SPIN * JACKPOT_CONTRIBUTION_RATE

        jackpot_win = 0

        # Hidden progressive jackpot trigger
        if random.random() < JACKPOT_TRIGGER_PROBABILITY:
            jackpot_hits += 1

            jackpot_win = jackpot_pool
            jackpot_total_paid += jackpot_win

            jackpot_pool = SEED_JACKPOT

        total_spin_win = base_win + jackpot_win

        total_bet += BET_PER_SPIN
        total_win += total_spin_win
        base_game_win += base_win

        spin_wins.append(total_spin_win)

        if total_spin_win > 0:
            hit_count += 1

        if base_win > 0:
            base_hit_count += 1

    final_rtp = total_win / total_bet
    base_rtp = base_game_win / total_bet
    jackpot_rtp = jackpot_total_paid / total_bet

    hit_frequency = hit_count / NUM_SPINS
    base_hit_frequency = base_hit_count / NUM_SPINS

    average_win = statistics.mean(spin_wins)
    standard_deviation = statistics.pstdev(spin_wins)

    print("Fantasy Progressive Jackpot Slot Simulation")
    print("------------------------------------------")
    print(f"Paid Spins: {NUM_SPINS:,}")
    print(f"Bet Per Spin: {BET_PER_SPIN}")
    print(f"Total Bet: {total_bet:,.2f}")
    print(f"Base Game Win: {base_game_win:,.2f}")
    print(f"Jackpot Total Paid: {jackpot_total_paid:,.2f}")
    print(f"Total Win: {total_win:,.2f}")
    print("------------------------------------------")
    print(f"Final RTP: {final_rtp:.2%}")
    print(f"Base Game RTP: {base_rtp:.2%}")
    print(f"Jackpot RTP: {jackpot_rtp:.2%}")
    print("------------------------------------------")
    print(f"Hit Frequency: {hit_frequency:.2%}")
    print(f"Base Hit Frequency: {base_hit_frequency:.2%}")
    print(f"Jackpot Hits: {jackpot_hits}")

    if jackpot_hits > 0:
        print(f"Jackpot Frequency: 1 in {NUM_SPINS / jackpot_hits:.2f} spins")
        print(f"Average Jackpot Paid: {jackpot_total_paid / jackpot_hits:,.2f}")
    else:
        print("Jackpot Frequency: No jackpot triggered")

    print(f"Current Jackpot Pool: {jackpot_pool:,.2f}")
    print(f"Visible 5+ Jackpot Symbol Occurrences: {visible_jackpot_5plus_count}")
    print("------------------------------------------")
    print(f"Average Win Per Spin: {average_win:.4f}")
    print(f"Standard Deviation: {standard_deviation:.4f}")


if __name__ == "__main__":
    run_simulation()
