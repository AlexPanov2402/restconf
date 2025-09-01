class Rpc_Handler:
    """
    Класс для обработки удалённых процедур (RPC).

    В этом классе реализуются методы, для примера возьмём трансляцию аудио потока
    - воспроизведение.
    - остановка воспроизведения.
    """

    def __init__(self):
        """
        Инициализация обработчика.
        """
        pass

    def play_song(self, input_data: dict) -> dict:
        """
        Воспроизведение по запросу.

        :param input_data: Словарь с параметрами, должен содержать ключ "song".
        :return: Словарь с состоянием воспроизведения, например, "Playing {song}".
        """
        # Получаем название аудио из входных данных, либо "unknown"
        song = input_data.get("song", "unknown")
        return {"status": f"Playing {song}"}

    def stop(self, input_data: dict) -> dict:
        """
        Остановка трансляции.

        :param input_data: Не используется, так как остановка не требует параметров.
        :return: Словарь с состоянием остановки.
        """
        return {"status": "Stopped"}
