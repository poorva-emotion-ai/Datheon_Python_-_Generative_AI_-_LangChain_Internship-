
from agent import student_agent

def main():
    print("\n=== StudyPilot-AI: Console Agent ===")
    print("Ask questions using web search, calculations,")
    print("or local text files. Type 'exit' to quit.\n")

    while True:
        try:
            query = input("You: ").strip()

            if query.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not query:
                continue

            print("\nAgent:")
            response = student_agent.run(query)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nRequest failed: {e}\n")

if __name__ == "__main__":
    main()
