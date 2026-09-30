from agent import gemini_model

print("Testing Gemini...")

response = gemini_model.generate(
    [{"role": "user", "content": "Say hello in one sentence."}]
)

print(response)