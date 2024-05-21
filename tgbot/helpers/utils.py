from datetime import datetime
import logging
import os


def create_absolute_path(source_path: str,
                         file_name: str | None = None,
                         file_format: str | None = None,
                         add_time: bool = False) -> str:
    full_file_path = source_path

    if file_name:
        full_file_path += file_name

    if add_time:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        full_file_path += f"-{formatted_datetime}"

    if file_format:
        full_file_path += f".{file_format}"

    absolute_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), full_file_path))

    return absolute_file_path


def remove_temporary_files(temporary_files_path: list[str]):
    for file_path in temporary_files_path:
        try:
            os.remove(file_path)
            logging.info(f"Removed temporary file: {file_path}")
        except Exception as e:
            logging.info(f"Error removing file {file_path}: {e}")