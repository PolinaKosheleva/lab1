import os
import sys
from mutagen import File as MutagenFile


def read_audio_metadata(file_path):
    """
    Читает метаданные аудиофайла (MP3, WAV).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Загружаем аудиофайл через mutagen
    audio = MutagenFile(file_path)
    if audio is None:
        raise ValueError("Не удалось прочитать файл. Формат не поддерживается или файл повреждён.")

    metadata = {}

    # Техническая информация
    if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
        metadata["Длительность"] = f"{audio.info.length:.2f} сек"

    if hasattr(audio, 'info') and hasattr(audio.info, 'bitrate') and audio.info.bitrate:
        metadata["Битрейт"] = f"{audio.info.bitrate // 1000} кбит/с"

    # Чтение тегов (Исполнитель, Альбом, Год)
    artist = audio.get('TPE1') or audio.get('artist') or audio.get('TPE2')
    album = audio.get('TALB') or audio.get('album')
    year = audio.get('TDRC') or audio.get('date') or audio.get('TYER')

    metadata["Исполнитель"] = str(artist[0]) if artist else "Не указан"
    metadata["Альбом"] = str(album[0]) if album else "Не указан"
    metadata["Год"] = str(year[0]) if year else "Не указан"

    return metadata


def main():
    if len(sys.argv) < 2:
        print("Использование: python read_metadata.py <путь_к_аудиофайлу>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        metadata = read_audio_metadata(file_path)
        print(f"\nМетаданные для {file_path}:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()