class Rpc_Handler:
    def __init__(self):
        pass

    def play_song(self, input_data: dict) -> dict:
        song = input_data.get("song", "unknown")
        return {"status": f"Playing {song}"}

    def stop(self, input_data: dict) -> dict:
        return {"status": "Stopped"}
