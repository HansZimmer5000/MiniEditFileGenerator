# MiniEdit File Generator

This python script creates a '.mn' (json) file that is readable by Mininets MiniEdit GUI editor. This helps to make the used network topology visible, e.g. for presentations. 

BEWARE as this generator is adjusted to the topology described in "SDN on ACIDs" from Curic et al. 2017. For use you may have to adjust the code. You then may want to share your customization via this repo (MR/PR/issues).

## Usage 

It was developed / run with python v3.8.2. For all other versions this might not work. 

```shell
./main.py

# or

python main.py
``'
