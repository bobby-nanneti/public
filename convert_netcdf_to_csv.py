import iris
import csv
from datetime import datetime
from datetime import timedelta

class NetCDFProcessor:

    def process_netcdf_file():
        netCDFFile = r"C:\Documents\poc\test_netcdf_file.nc"
        listOfCubes = iris.load(netCDFFile)

        for cube in listOfCubes:

            try:
                longname = cube.long_name
                standard_name = cube.standard_name
                varname = cube.var_name
                justname = cube.name()

                coord_names = [coord.name() for coord in cube.coords()]
                # Get dimension coordinates
                dimCords = cube.dim_coords
                dim_names = [dimension.standard_name for dimension in cube.dim_coords]
                a = cube.coord('time')
                scalar_coordinate_time = a.points[0]
                measure_timestamp = gettimestamp(scalar_coordinate_time)
                log_date = measure_timestamp.date()

                realization = cube.coord(dimCords[0].standard_name).points
                latitudes = cube.coord(dimCords[1].standard_name).points
                longitudes = cube.coord(dimCords[2].standard_name).points

                csvHeaderList = []
                lastColumnName = "measure value"
                # Write to CSV file
                localCSVFileName = r"C:\\Documents\poc\testbobby.csv"
                with open(localCSVFileName, 'w', newline='') as csvFile:
                    csvFileWriter = csv.DictWriter(csvFile, delimiter='|', fieldnames=csvHeaderList)
                    csvHeaderList.append('log_date')
                    csvHeaderList.append('time')
                    csvHeaderList.append(dimCords[0].standard_name)
                    csvHeaderList.append(dimCords[1].standard_name)
                    csvHeaderList.append(dimCords[2].standard_name)
                    csvHeaderList.append(lastColumnName)
                    csvFileWriter.writeheader()
                    for i in range(18): ##range(cube.shape[1]):
                        for j in range(200): ##range(cube.shape[2]):
                            for k in range(400):
                                rowDict = {}
                                rowDict['log_date'] = log_date
                                rowDict['time'] = measure_timestamp
                                rowDict[dimCords[0].standard_name] = realization[i]
                                rowDict[dimCords[1].standard_name] = latitudes[j]
                                rowDict[dimCords[2].standard_name] = longitudes[k]
                                rowDict[lastColumnName] = cube.data[i][j][k]
                                csvFileWriter.writerow(rowDict)
            except Exception as e:
                print (e)


def gettimestamp(seconds_since_1970):
    try:
        minutes_since_1970 = seconds_since_1970 / 60
        baseline_date = "1970-01-01"
        Begindate = datetime.strptime(baseline_date, "%Y-%m-%d")
        EnddateTime = Begindate + timedelta(minutes=minutes_since_1970)
        return  EnddateTime
    except Exception as e:
        print(e)

if __name__ == "__main__":
    NetCDFProcessor.process_netcdf_file()
