import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! The Name Is Clown"


tokens = encoder.encode(text=text)
print(tokens)


decoded_text = encoder.decode(tokens)
print(decoded_text)

