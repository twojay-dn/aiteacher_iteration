import argparse
import openai as OAI
import os
from dotenv import load_dotenv

load_dotenv()
oai = OAI.OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def main(args):
  file_path = args.input
  file = 
  response = oai.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "user", "content": "What is the weather in Tokyo?"}
    ]
  )
  print(response.choices[0].message.content)
  write_in_file(args.input, response.choices[0].message.content)
  
def write_in_file(path : str, content : str):
  with open(path, "w", encoding="utf-8") as f:
    f.write(content)

if __name__ == "__main__":
  args = argparse.ArgumentParser()
  args.add_argument("--input", type=str, required=True)
  args.add_argument("--n", type=int, required=True)
  args = args.parse_args()
  args.input = f"{os.getcwd()}/{args.input}"
  main(args)
