from openai import OpenAI

client = OpenAI(api_key='Your OPENAI API Key goes here')
import re

# Initialize OpenAI with your API key

def translate_text(text, source_lang, target_lang):
    try:
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Translate the following text from {source_lang} to {target_lang}."},
            {"role": "user", "content": text}
        ],
        max_tokens=2000  # Adjust based on the maximum limit and the length of expected response)
)
        translation = response.choices[0].message.content
        return translation.strip()
    except Exception as e:
        print(f"Error occurred during translation: {str(e)}")
        raise

def translate_srt_file(input_file, output_file, source_lang, target_lang):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            srt_content = file.read()

        # Regular expression to match SRT blocks
        srt_pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n(?=\d+\n|$)', re.DOTALL)
        blocks = srt_pattern.findall(srt_content)

        total_blocks = len(blocks)

        with open(output_file, 'a', encoding='utf-8') as out_file:
            for i, block in enumerate(blocks):
                index, start_time, end_time, text = block
                try:
                    translated_text = translate_text(text, source_lang, target_lang)
                    out_file.write(f"{index}\n{start_time} --> {end_time}\n{translated_text}\n\n")
                except Exception as e:
                    print(f"Error occurred during translation of block {index}: {str(e)}")
                    raise

                # Print progress
                progress = min(100, int((i + 1) / total_blocks * 100))
                print(f"Translated {progress}%")

        print("Translation complete.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    input_srt = 'input.srt'
    output_srt = 'output_translated.srt'
    source_language = 'English'
    target_language = 'Arabic'

    print(f"Starting translation from {source_language} to {target_language}...")
    translate_srt_file(input_srt, output_srt, source_language, target_language)

