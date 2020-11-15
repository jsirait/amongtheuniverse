import csv
import pandas as pd
import json
import random
import requests

URL = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=pl_name,pl_discmethod,pl_orbper,pl_radj,pl_bmassj,pl_dens"
jupyter_mass = 1.898*(10**27) # in kg
earth_mass = 5.972*(10**24)
jupyter_rad = 43441
earth_rad = 3958.8 # in miles
einj_mass = jupyter_mass/earth_mass
einj_rad = jupyter_rad/earth_rad


def generateRandomPl():
    df = pd.read_csv("nph-nstedAPI.csv")
    df = df.dropna()
    num_pl = df.shape
    k = random.randint(1,num_pl[0]+1)
    planet = df.iloc[k]
    return planet

def specificPlanetData(planetName):
    df = pd.read_csv("nph-nstedAPI.csv")
    data = df[df['pl_name']==planetName]
    return data

def list_rad():
    df = pd.read_csv("nph-nstedAPI.csv")
    df_earth = df[abs(df['pl_radj']*einj_rad-1)<0.2]
    return df_earth

def list_mass():
    df = pd.read_csv("nph-nstedAPI.csv")
    df_earth = df[abs(df['pl_bmassj']*einj_mass-1)<0.2]
    return df_earth

def list_orb():
    df = pd.read_csv("nph-nstedAPI.csv")
    df_earth = df[abs(df['pl_orbper']-365)<30]
    return df_earth

def listAll():
    df = pd.read_csv("nph-nstedAPI.csv")
    return df

if __name__ == "__main__":
    print(generateRandomPl())
    # print(type(specificPlanetData("KOI-55 c")))
    print(specificPlanetData("KOI-55 c"))