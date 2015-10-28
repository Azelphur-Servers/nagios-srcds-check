# nagios-srcds-check
Check SRCDS servers using RCON

This is a simple python script which we will use to let nagios know about the status of our servers, currently it reports...

- Number of humans playing
- Number of bots playing
- Maximum players
- Current map
- The status of replay
- Average player loss
- Average player ping
- Check that sm version command works
- Check that meta version command works

# Installing
You'll need python-valve, which you can get by running
```
git clone https://github.com/Holiverh/python-valve.git
cd python-valve
sudo python setup.py install
```
