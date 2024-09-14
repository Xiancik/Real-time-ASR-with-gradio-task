# Real streaming ASR with gradio task
I also provided a model already for easier testing and example, but you could use any other ASR model you would like
## Installation
You can extract the files from the attached .zip or from the following github repository: 

You can install the needed python libraries using the package manager [pip](https://pip.pypa.io/en/stable/) :
```bash
pip install sherpa_onnx
pip install numpy
pip install asyncio
pip install websockets
pip install gradio
```

## Running
To run the server and gradio app, you should first enter in the repository in cmd and then type the following command in cmd:
```bash
python3.12 ./codes/streaming_server.py --encoder ./sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/encoder-epoch-99-avg-1.onnx --decoder ./sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/decoder-epoch-99-avg-1.onnx --joiner ./sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/joiner-epoch-99-avg-1.onnx --tokens ./sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/tokens.txt
```

This command will pass as arguments the used encoder, decoder, joiner and the tokens. It is not necessary to use the one provided as an example, just make sure you pass the correct paths.

After you used the command, after waiting a bit for the setup, in cmd should appear the address of the gradio app:
```bash
Running on local URL:  http://127.0.0.1:7860
```
Copy it and put it in the search bar of the browser. Now you can use the app. 