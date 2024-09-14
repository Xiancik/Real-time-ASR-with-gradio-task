import gradio as gr
import numpy as np
import asyncio
import websockets
import json

def downsample(arr,rs) :
  """A method to downsample the initial 
  audio data to the sample rate required by the server

  Parameters: 
  arr - the float32 array audio           
  rs - the sample rate of the audio

  Returns:
  array of float32 - the downsampled audio
  """

  if rs == 16000:
    return arr
  
  ratio = rs / 16000
  newlen = round(len(arr) / ratio)
  result = np.zeros(newlen,dtype=np.float32)
  offr = 0
  offsetarr = 0
  while offr < len(result) :
    nextoffarr = round((offr + 1) * ratio)
    acc = 0 
    count = 0
    for i in range(offsetarr,min(nextoffarr,len(arr))):
      acc += arr[i]
      count+=1
    result[offr] = acc / count
    offr+=1
    offsetarr = nextoffarr
  return result


class WebSocketHandler:
    """
    A websocket class to handle the transfer of data and the connections
    """
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.connecting = asyncio.Lock() 

    async def connect(self):
        async with self.connecting:  
            if self.websocket is None or self.websocket.closed:
                try:
                    self.websocket = await websockets.connect(self.uri)
                    print("Connected to WebSocket")
                except Exception as e:
                    print(f"Failed to connect to WebSocket: {e}")

    async def send(self, data):
        try:
            if self.websocket is None or self.websocket.closed:
                await self.connect()

            if self.websocket is not None:
                await self.websocket.send(data.tobytes())           
        except Exception as e:
            print(f"WebSocket error: {e}")
            await self.close()
            return None
    async def receive(self):
       if self.websocket is None or self.websocket.closed:
                await self.connect()
       while True:
          message = self.websocket.recv()
          if message is not None:
             return message
    async def close(self):
        self.websocket.close()

messages = {}
socket = WebSocketHandler("ws://localhost:6006")

async def transcribe(new_chunk):
    """The method which we will pass to the gradio
    interface to process the audio

    Parameters:
    new_chunk - the audio recorded, a tuple of the form (int, array)

    Returns:
    string - the text that should be displayed, contains all the previous processed audio
    """
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))
    y = downsample(y,sr)
    message = await socket.send(y)
    s = ""
    for x in messages.keys():
        s = s + messages[x]+ "\n"
    return s
        

async def checker(swocket = socket):
   """The method to constantly check the websocket for incoming data
  If we got a message we put it in the dictionary respective to its segment value
   """
   await swocket.connect()
   while True:
      message = await swocket.websocket.recv()
      message = json.loads(message)
      if message is not None and message["text"]!="":
        messages[message["segment"]]=message["text"]
         
def starter():
    """The method which is called in the server side to start the gradio app
    This method also runs the checker and totalstart(where the actual gradio starts) concurrently
    """
    asyncio.gather(asyncio.create_task(checker(socket)),asyncio.create_task(totalstart()))
async def totalstart():
    demo = gr.Interface(
        transcribe,
        [gr.Audio(sources=["microphone"], streaming=True)],
        ["text"],
        live=True,
    )

    demo.launch(prevent_thread_lock=True)
