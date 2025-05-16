from TTG_Backend.challenges import CHALLENGES
from TTG_Backend.board_encoder import BoardEncoder
from TTG_Backend.AIChallengeSolver import TransformerPlanner

def solve_challenge(challenge_id, challenge):
    board = challenge["board"]
    encoder = BoardEncoder()
    planner = TransformerPlanner()
    encoded_state = encoder.encode_board(board)
    plan = planner.plan(encoded_state)
    steps = planner.parse_plan(plan)
    return plan, steps

def main():
    print(f"Found {len(CHALLENGES)} challenges.")
    for challenge_id, challenge in CHALLENGES.items():
        print(f"\n=== Solving Challenge: {challenge_id} ===")
        print(f"Description: {challenge.get('description', '')}")
        plan, steps = solve_challenge(challenge_id, challenge)
        print("AI Plan:")
        print(plan)
        print("Parsed Steps:")
        for step in steps:
            print(f"Place {step[0].name} at ({step[1]}, {step[2]})")

if __name__ == "__main__":
    main() 