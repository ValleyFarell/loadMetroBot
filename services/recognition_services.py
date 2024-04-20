import os

def voice_to_text(file_path: str, output_path: str) -> str:
    os.system(f'vosk-transcriber -l ru -i {file_path} --output {output_path}')
