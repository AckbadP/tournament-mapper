# Tournament Mapper
## Author
    Ackbad Pappotte

## Dependancies
 - pytorch: https://pytorch.org/get-started/locally/
 - GPU:
    - if AMD gpu, RCOM: https://rocm.docs.amd.com/en/latest/
    - if NVIDA gpu, CUDA:
    - can also use default of cpu, but will be slower

## About

## Designe
### Visuilizer
Build the visuilizer in a game engine like godot or unity

### Reader
Build computer vision reader in python
Assume all videos will be pre-synced and combine into one file
reader.py reades a static image pulled from vid by visulizer.py and returns data from image
visulizer.py gets 1 image for every second of vid for data