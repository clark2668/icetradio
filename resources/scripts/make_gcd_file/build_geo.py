from icecube import icetray, dataclasses, dataio
import os
import numpy as np

import argparse
parser = argparse.ArgumentParser()
defaultloc = "locations.dat"
parser.add_argument('-i', '--input', type=str, default=defaultloc, help='path to antenna location information')
args = parser.parse_args()

#Fills the radio geometry objects with the correct valuess
def MakeAntennaGeo(antFile, iAnt):

	x = antFile['CenterX'][iAnt]
	y = antFile['CenterY'][iAnt]
	z = antFile['CenterZ'][iAnt]
	OrientationTheta = np.deg2rad(antFile['OrientationTheta'][iAnt])
	OrientationPhi = np.deg2rad(antFile['OrientationPhi'][iAnt])
	RotationTheta = np.deg2rad(antFile['RotationTheta'][iAnt])
	RotationPhi = np.deg2rad(antFile['RotationPhi'][iAnt])
	AntennaType = antFile['AntennaType'][iAnt]
	AntennaModel = antFile['AntennaModel'][iAnt]

	iceantennaGeo = dataclasses.I3IceAntennaGeo()
	iceantennaGeo.position = dataclasses.I3Position(x, y , z)

	# # FIXME! This is using the zenith and azimuth constructor, but I'm giving it in terms of theta and phi!
	iceantennaGeo.orientation = dataclasses.I3Direction(OrientationTheta, OrientationPhi)
	iceantennaGeo.rotation = dataclasses.I3Direction(RotationTheta, RotationPhi)

	if AntennaType=='dipole':
		iceantennaGeo.antennaType = dataclasses.I3IceAntennaGeo.IceAntennaType.dipole
	elif AntennaType=='lpda':
		iceantennaGeo.antennaType = dataclasses.I3IceAntennaGeo.IceAntennaType.lpda

	iceantennaGeo.antennaModel = AntennaModel

	return iceantennaGeo

# actually makes the G frame
def MakeGeometryFrame(antFile):
	antFile = np.genfromtxt(args.input, delimiter=',',names=True, dtype=None,encoding='ASCII')
	print("Reading in deployed locations from: ", args.input)

	frame = icetray.I3Frame(icetray.I3Frame.Geometry)
	antGeometry = dataclasses.I3Geometry()

	num_ants = len(antFile['StationID'])

	for iAnt in range(num_ants):
		stationID = int(antFile['StationID'][iAnt])
		antennaID = int(antFile['AntennaID'][iAnt])
		antkey = dataclasses.IceAntennaKey(stationID, antennaID)
		antennaGeo = MakeAntennaGeo(antFile, iAnt)
		antGeometry.iceantennageo[antkey] = antennaGeo

	# print(antGeometry.iceantennageo)
	frame['I3IceAntennaGeometry'] = antGeometry
	return frame

# makes a dummy C frame
def MakeCalibrationFrame():
	frame = icetray.I3Frame(icetray.I3Frame.Calibration)
	return frame

# makes a dummy D frame
def MakeDetectorStatusFrame():
	frame = icetray.I3Frame(icetray.I3Frame.DetectorStatus)
	return frame

i3file = dataio.I3File("sampleGCD.i3.gz","w")
antFile = args.input
i3file.push(MakeGeometryFrame(antFile))
i3file.push(MakeCalibrationFrame())
i3file.push(MakeDetectorStatusFrame())
i3file.close()

