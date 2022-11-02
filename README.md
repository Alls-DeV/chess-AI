Chess game written in python with the pygame library.  The chess engine uses the minimax search tree, with alpha-beta pruning to reduce search times, to find the best move based on the following heuristics:

* material
* position of the piece
* number of possible legal moves

## Setup Instructions
###### Make sure you're using python 3

### Debian
```bash
sudo apt install python3-pip
pip3 -m install --user pygame
python3 main.py
```

### Arch
```bash
sudo pacman -S python-pip
pip -m install --user pygame
python main.py
```
###### If pygame fails to install try:

###### `sudo pip3 install pygame` (Ubuntu)

###### `sudo pip install pygame` (Arch)

###### also, maybe will help:

###### `sudo pip install --upgrade-pip`

### Windows

[python](https://www.python.org/downloads)

###### Make sure to add python to your PATH

Then, Open a command prompt window:
```
pip -m install --user pygame
python main.py
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

