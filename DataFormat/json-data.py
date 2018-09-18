#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pprint

class processJSON:
    def __init__( self ):
        self.author = "Manish Pandit, updatedmanish@gmail.com"
    
    def writeJSONFile( self, data, targetOutput ):
        with open( targetOutput, 'w' ) as outputFile:
            json.dump( data, outputFile, indent = 4 )
    
    def readJSONFile( self, fileName ):
        with open( fileName, 'r' ) as inputFile:
            fileContent = json.load( inputFile )
        return fileContent


if __name__ == "__main__":
    pp = pprint.PrettyPrinter( indent = 4 )
    dataProcess = processJSON()
    json_data = {
        "researcher": {
            "name": "Ford Prefect",
            "species": "Betelgeusian",
            "relatives": [
                {
                    "name": "Zaphod Beeblebrox",
                    "species": "Betelgeusian"
                }
            ]
        }
    }

    json_string = """
    {
        "researcher": {
            "name": "Ford Prefect",
            "species": "Betelgeusian",
            "relatives": [
                {
                    "name": "Zaphod Beeblebrox",
                    "species": "Betelgeusian"
                }
            ]
        }
    }
    """
    fileContent = dataProcess.readJSONFile( 'output/input.json' )
    pp.pprint( fileContent )
    dataProcess.writeJSONFile( fileContent, 'output/output.json' )