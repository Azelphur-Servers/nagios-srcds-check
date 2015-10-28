#!/usr/bin/python
from valve.source.rcon import RCON
import argparse
import re

re_status_players = re.compile('^players\s+\:\s+(?P<humans>\d+) humans, (?P<bots>\d+) bots \((?P<max>\d+) max\)$')
re_status_map = re.compile('^map\s+\:\s+(?P<map>.+) at\: \d+ x, \d+ y, \d+ z$')
re_status_replay = re.compile('^replay\s+\:\s+(?P<status>.+)$')
re_status_player = re.compile('^#\s+(?P<userid>\d+)\s+"(?P<name>.+)"\s+(?P<uniqueid>\[U\:\d\:\d+\])\s+(?P<connected>[0-9\:]+)\s+(?P<ping>\d+)\s+(?P<loss>\d+)\s+(?P<state>.+)\s+(?P<adr>.+)$')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('hostname', type=str, help='Server IP/Hostname')
parser.add_argument(
    'port',
    type=int,
    default=27015,
    help='Server Port (Default: 27015)'
)
parser.add_argument(
    'rcon_password',
    type=str,
    help='RCON Password, if supplied the script will run rcon status instead of A2S_INFO.'
)
args = parser.parse_args()

if args.rcon_password:
    with RCON((args.hostname, args.port), args.rcon_password) as rcon:
        status = rcon('status')
        pings = []
        losses = []
        for line in status.splitlines():
            match = re_status_players.match(line)
            if match:
                print('Humans: %s' % (match.group('humans'),))
                print('Bots: %s' % (match.group('bots'),))
                print('MaxPlayers: %s' % (match.group('max'),))
            match = re_status_map.match(line)
            if match:
                print('Map: %s' % (match.group('map'),))
            match = re_status_replay.match(line)
            if match:
                print('Replay: %s' % (match.group('status'),))
            match = re_status_player.match(line)
            if match:
                pings.append(int(match.group('ping')))
                losses.append(int(match.group('loss')))
        print('AvgLoss: %d' % (sum(losses)/len(losses),))
        print('AvgPing: %d' % (sum(pings)/len(pings),))
        if 'SourceMod Version Information' in rcon('sm version'):
            print('SourceMod: true')
        else:
            print('sourceMod: false')
        if 'Metamod:Source version' in rcon('meta version'):
            print('MetaMod: true')
        else:
            print('MetaMod: false')
