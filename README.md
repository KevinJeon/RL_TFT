# Teamfight Tactics(TFT) for Machine Learning 

Follow the command to test the environment.

```bash
docker build -t rl_tft .
docker run -it -e "DISPLAY" -v /tmp/.X11-unix/:/tmp/.X11-unix/ rl_tft 

# In case, you're running on Windows system, make sure that a X dispaly server is installed, such as Xming.
```

## TODOs
- [ ] Modularize a big file into smaller pieces.
- [ ] Make use of Environment variables for configuration.
- [ ] Extend this Todo list.
- [ ] Make Pathfinder.
- [ ] Update View File

