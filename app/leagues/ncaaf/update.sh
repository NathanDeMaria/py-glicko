#!/usr/bin/env bash
set -e

# Assumes you have https://github.com/NathanDeMaria/EndGame cloned next to py-glicko
Rscript ../../../../EndGame/applications/ncaaf/ncaa_fb.R
if [ ! -f ncaaf_team_info.csv ]
then
Rscript ../../../../EndGame/applications/ncaaf/cfb_teams.R
fi
# TODO: include generation of ncaaf_recruiting.csv, make above check once a year

python subdivisions.py
