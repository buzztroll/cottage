import subprocess


def play_audio(audio_file):
    subprocess.run(f"mpg123 {audio_file}", shell=True, check=True)

