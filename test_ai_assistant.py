from ai_assistant import extract_journey, generate_response

message = input("Enter your journey or request: ")

result = extract_journey(message)

print("\nAI Result:", result)

if result["intent"] == "sos":

    print("\nSOS detected! Emergency assistance requested.")

else:

    reply = generate_response(
        result["language"],
        result["source"],
        result["destination"]
    )

    print("\nAI Reply:", reply)