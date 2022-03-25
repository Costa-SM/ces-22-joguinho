import imp


from csv import reader

def importCsvLayout(path):
    '''
    Function that imports our .csv level layout
    :param path: the .csv file path.
    :type levelData: string.
    :rtype: list.
    
    '''
    terrainMap = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrainMap.append(list(row))
        return terrainMap
