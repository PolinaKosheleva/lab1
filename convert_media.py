import os
import shutil
import subprocess
import sys


def check_ffmpeg():
    """Проверяет наличие FFmpeg в системе."""
    if shutil.which('ffmpeg') is None:
        print("Ошибка: FFmpeg не найден. Установите FFmpeg и добавьте его в PATH.")
        return False
    return True


def convert_wav_to_mp3(input_path, output_path):
    """Конвертирует WAV в MP3 с помощью FFmpeg."""
    if not os.path.exists(input_path):
        print(f"Ошибка: Входной файл '{input_path}' не найден.")
        return False

    if not check_ffmpeg():
        return False

    cmd = ['ffmpeg', '-i', input_path, '-y', output_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Конвертация завершена! Создан файл: {output_path}")
            return True
        else:
            print(f"Ошибка FFmpeg:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"Ошибка запуска процесса: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("Использование: python convert_media.py <входной_file.wav> <выходной_file.mp3>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    convert_wav_to_mp3(input_path, output_path)


if __name__ == '__main__':
    main()