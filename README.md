# imagestory.ai

**imagestory.ai** is a simple AI website that writes stories based on a given image.

![imagestoryai0](https://github.com/gnud-gnaoh/imagestory.ai/assets/104649178/f84ff703-ac4a-4a72-a3f8-116db99c6cd5)
![imagestoryai1](https://github.com/gnud-gnaoh/imagestory.ai/assets/104649178/0c5aa444-a7b6-4a8d-ab3f-52f3e1369576)

Uses [Flask](https://flask.palletsprojects.com/en/2.3.x/) for back-end, [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) for front-end.

Uses [nlpconnect/vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) for image-to-text, [TheBloke/orca_mini_3B-GGML](https://huggingface.co/TheBloke/orca_mini_3B-GGML) for text generation.

## Installation & usage

- (Optional) Create a virtual environment

Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```
    
Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

If there is error with "Execution Policies", run:
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install require packages.
```bash
pip install -r requirements.txt
```

- Create folder `static/uploads`
```bash
mkdir static/uploads
```

- To run:
```bash
flask run 
```

## Project Structure

- `templates/`: html files
- `static/`: images, uploaded files

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
