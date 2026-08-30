import asyncio
import json
import websockets


players = set()

board = [
    "", "", "",
    "", "", "",
    "", "", ""
]

current_player = "X"


async def broadcast_state():
    state = {
        "board": board,
        "current_player": current_player
    }

    message = json.dumps(state)

    for player in players:
        await player.send(message)


async def handler(websocket):
    global current_player

    players.add(websocket)

    try:
        await websocket.send(json.dumps({
            "board": board,
            "current_player": current_player
        }))

        async for message in websocket:
            data = json.loads(message)

            position = data.get("position")
            symbol = data.get("symbol")

            if (
                position is not None
                and 0 <= position <= 8
                and board[position] == ""
                and symbol == current_player
            ):
                board[position] = symbol

                if current_player == "X":
                    current_player = "O"
                else:
                    current_player = "X"

                await broadcast_state()

    finally:
        players.remove(websocket)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer gry działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
