from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import FractalWorld
from CvMapGeneratorUtil import TerrainGenerator
from CvMapGeneratorUtil import FeatureGenerator
import random

def getDescription():
	return "TXT_KEY_MAP_SCRIPT_ANEWWORLD_DESCR"
	
def isAdvancedMap():
	"This map should show up in simple mode"
	return 0

def getWrapX():
	return false
	
def getWrapY():
	return false

def generatePlotTypes():
	NiTextOut("Setting Plot Types (Python Fractal) ...")
	fractal_world = FractalWorld( 4, 4 )
	fractal_world.initFractal(continent_grain = 3, rift_grain = 4, has_center_rift = False, polar = True)
	retVal = fractal_world.generatePlotTypes(70)
	sinkEasternShore(fractal_world, 4)
	sinkWesternShore(fractal_world, 4)
	setWestEurope()
	return retVal

def generateTerrainTypes():
	NiTextOut("Generating Terrain (Python Fractal) ...")
	terraingen = MyTerrainGenerator(grain_amount=6)
	terrainTypes = terraingen.generateTerrain()
	return terrainTypes

def addFeatures():
	NiTextOut("Adding Features (Python Fractal) ...")
	featuregen = FeatureGenerator()
	featuregen.addFeatures()
	return 0
	
def sinkEasternShore(fractal_world, iWidth):
	for x in range(iWidth):
		for y in range(fractal_world.iNumPlotsY):
			i = y * fractal_world.iNumPlotsX + fractal_world.iNumPlotsX - 1 - x 
			fractal_world.plotTypes[i] = PlotTypes.PLOT_OCEAN
				
	return 0

def sinkWesternShore(fractal_world, iWidth):
	for x in range(iWidth):
		for y in range(fractal_world.iNumPlotsY):
			i = y * fractal_world.iNumPlotsX + x 
			fractal_world.plotTypes[i] = PlotTypes.PLOT_OCEAN
				
	return 0


def setWestEurope():
	map = CyMap()
	gc = CyGlobalContext()
	europeWest = gc.getInfoTypeForString("EUROPE_WEST")
	#noEurope = gc.getInfoTypeForString("NO_EUROPE")
	for iY in range(map.getGridHeight()):
		myPlot = map.plot(0,iY)
		myPlot.setEurope(europeWest)
	

def findStartingPlot(argsList):
	"Can override to return the plot index at which the given player should start"
	playerID = argsList[0]
	
	gc = CyGlobalContext()
	map = CyMap()
	player = gc.getPlayer(playerID)
	
	player.AI_updateFoundValues(True)
	
	if player.getCivilizationDescriptionKey()=='TXT_KEY_CIV_CHINA_DESC':
		bp = player.findStartingPlot(false)
		y =bp.getY()
		x = 0
		for x in range(0,3):
			myPlot = map.plot(x+1,y)
			if myPlot.isEurope() ==  False:
				break
			x = x + 1
		return map.plotNum(x, y)
	else:
		bp=player.findStartingPlot(false)
		return map.plotNum(bp.getX(),bp.getY())

def afterGeneration():
	map = CyMap()
	#noEurope = gc.getInfoTypeForString("NO_EUROPE")
	for iY in range(map.getGridHeight()):
		myPlot = map.plot(4,iY)
		myPlot.setEurope(-1)
		myPlot1 = map.plot(5,iY)
		myPlot1.setEurope(-1)		
	
	


class MyTerrainGenerator(TerrainGenerator):

	def generateTerrainAtPlot(self,iX,iY):
		lat = self.getLatitudeAtPlot(iX,iY)
	
		plot = self.map.plot(iX, iY)
	
		if (plot.isWater()):
			return self.map.plot(iX, iY).getTerrainType()
		terrainVal = self.terrainGrass
		r = random.randint(1,11)
		if r < 1:
			terrainVal = self.terrainMarsh
		elif r>9:
			terrainVal = self.terrainPlains
		if lat >= self.fSnowLatitude:
			terrainVal = self.terrainIce
		elif lat >= self.fTundraLatitude:
			terrainVal = self.terrainTundra
		elif lat < self.fGrassLatitude:
			terrainVal = self.terrainGrass
		else:
			desertVal = self.deserts.getHeight(iX, iY)
			plainsVal = self.plains.getHeight(iX, iY)
			marshVal = self.marsh.getHeight(iX, iY)
			if ((desertVal >= self.iDesertBottom) and (desertVal <= self.iDesertTop) and (lat >= self.fDesertBottomLatitude) and (lat < self.fDesertTopLatitude)):
				terrainVal = self.terrainDesert
			elif ((marshVal >= self.iMarshBottom) and (marshVal <= self.iMarshTop) and plot.isFlatlands() and (lat >= self.fDesertBottomLatitude) and (lat < self.fDesertTopLatitude)):
				terrainVal = self.terrainMarsh
			elif ((plainsVal >= self.iPlainsBottom) and (plainsVal <= self.iPlainsTop)):
				terrainVal = self.terrainPlains
	
		if (terrainVal == TerrainTypes.NO_TERRAIN):
			return self.map.plot(iX, iY).getTerrainType()
	
		return terrainVal
			
		
	

