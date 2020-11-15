from flask import Flask, render_template, request
import funcs
import json
import math

jupyter_mass = 1.898*(10**27) # in kg
earth_mass = 5.972*(10**24)
jupyter_rad = 43441
earth_rad = 3958.8 # in miles
einj_mass = jupyter_mass/earth_mass
einj_rad = jupyter_rad/earth_rad

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forWorlds/')
def forWorlds():
    return render_template('forWorlds.html')

@app.route('/randomPlanet/')
def randomPlanet():
    planet = funcs.generateRandomPl()
    pl_name = planet['pl_name']
    pl_discmethod = planet['pl_discmethod']
    pl_orbper = planet["pl_orbper"]
    pl_radj = planet['pl_radj']*10.973
    pl_bmassj = planet["pl_bmassj"]*317.8165
    pl_dens = planet["pl_dens"]
    return render_template('planetPage.html', 
        pl_name = pl_name, pl_discmethod = pl_discmethod,
        pl_orbper = pl_orbper, pl_radj = pl_radj,
        pl_bmassj = pl_bmassj, pl_dens = pl_dens,
        planet = planet)

@app.route('/planet/<planetName>/')
def specificPlanet(planetName):
    data = funcs.specificPlanetData(planetName)
    for _,planet in data.iterrows():
        pl_name = planet['pl_name']
        pl_discmethod = planet['pl_discmethod']
        pl_orbper = planet["pl_orbper"]
        pl_radj = planet['pl_radj']*10.973
        print(type(pl_radj))
        pl_bmassj = planet["pl_bmassj"]*317.8165
        pl_dens = planet["pl_dens"]
    if math.isnan(pl_orbper):
        pl_orbper="(unknown)"
    if math.isnan(pl_bmassj):
        pl_bmassj = "(unknown)"
    if math.isnan(pl_dens):
        pl_dens="(unknown)"
    if math.isnan(pl_radj):
        pl_radj="(unknown)"
    return render_template('planetPage.html', 
        pl_name = pl_name, pl_discmethod = pl_discmethod,
        pl_orbper = pl_orbper, pl_radj = pl_radj,
        pl_bmassj = pl_bmassj, pl_dens = pl_dens,
        planet = planet)

@app.route('/planetList/<ref>')
def planetList(ref):
    thelist = None
    planetTable = dict()
    table_title = "Discovered Planets"
    if ref=="mass":
        thelist = funcs.list_mass()
        table_title = "Planets with similar mass as the Earth"
    elif ref=="size":
        thelist = funcs.list_rad()
        table_title = "Planets with similar size as the Earth"
    elif ref=="orb":
        thelist = funcs.list_orb()
        table_title = "Planets with similar orbital period as the Earth"
    else:
        thelist = funcs.listAll()
    if not thelist.empty:
        for _,row in thelist.iterrows():
            temp = dict()
            temp['radius'] = row["pl_radj"]*einj_rad
            temp['mass'] = row["pl_bmassj"]*einj_rad
            temp['orbital period'] = row['pl_orbper']
            temp['density'] = row['pl_dens']
            temp['discovery method'] = row['pl_discmethod']
            planetTable[row["pl_name"]] = temp
    num_planets = len(planetTable)
    return render_template('planetLists.html',
        planetTable=planetTable,
        table_title = table_title,
        num_planets = num_planets)

@app.route('/motivationabout/')
def motivationabout():
    return render_template("motivationabout.html")

if __name__ == "__main__":
    app.debug = True
    app.run()