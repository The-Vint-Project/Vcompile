class VINTFile():

    def __init__(self, fileName: str) -> None:
        self.__fileName = fileName
        self.__fileObject = open(fileName, "a+")
        self.__fileObject.seek(0)
        self.__fileContentsI = self.__fileObject.read()
        self.fileContents = self.__fileContentsI
        self.__options = {
            "CATCODES": [
                ["\\"],  # Start Command 0
                ["{"],  # Start Group 1
                ["}"],  # End Group 2
                ["@"],  # Mode Switch 3
                ["\n", "\r"],  # End Of Line 4
                [" ", "\t"],  # Spacer 5
                ["&"],  # Alignment char 6
                ["$"],  # Variable marker 7
                [],  # Short Command - langauge defined 8
                ["%"],  # Comment 9
                [],  # Other 10
                [],  # Invalid 11
                [],
                []
            ],
            "COMMANDCODES": [  # Langauge defined, in VINT =-+^_()[]:|<>~-≈#*`
            ],
            "age": 18,
            "name": "Luca Di Bona"
        }
        self.__statements = []

    def parse(self) -> None:

        def parseStatement(self, statement: str, spacer: str = "") -> None:
            pass

            def getCatCode(self, char: str) -> int:
                """
                Generates the category code of a character

                Args:
                    char (char): the character analysed

                Returns:
                    int: the category code of the character

                """

                for i,val in enumerate(self.__options["CATCODES"]):
                    for j in val:
                        if char == j:
                            return(i)

            curCatCode = 0
            curStatement = ""
            curSpacer = ""
            thing = [["",""]]
            statementMode = True #statement mode or spacer mode
            groupLevel = 0
            line = 0

            self.fileContents += "X" #adds an extra character to text that will be processed
            for i in self.fileContents:

                prevCatCode = curCatCode
                curCatCode = getCatCode(self,i)

                if statementMode:

                    if i in (self.__options["CATCODES"][5] + self.__options["CATCODES"][4]): #Spacer or new line
                        if i in self.__options["CATCODES"][4]:
                            line += 1
                        statementMode = False
                        if len(thing[groupLevel]) == 1:
                            thing[groupLevel].append('')
                        thing[groupLevel][1] += i
                        curSpacer += i

                    elif i in self.__options["CATCODES"][1]: #Start Group
                        groupLevel += 1
                        curStatement += i
                        if len(thing) <= groupLevel:
                           thing.append([''])
                        thing[groupLevel][0] += i

                    elif i in self.__options["CATCODES"][2]: #End Group
                        groupLevel -= 1
                        if groupLevel < 0:
                            raise Exception(f"Closing brace without matching opening brace on line {line}")
                        else:
                            self.__statements.append([curStatement,""])
                            curStatement = i
                            curSpacer = ''
                            thing[groupLevel][0] = i

                    elif curCatCode == prevCatCode:
                        curStatement += i
                        thing[groupLevel][0] += i

                    else:
                        self.__statements.append([curStatement,""])
                        curStatement = i
                        curSpacer = ''
                        thing[groupLevel][0] = i

                else:

                    if i in self.__options["CATCODES"][5]: #Spacer
                        thing[groupLevel][1] += i
                        curSpacer += i

                    elif i in self.__options["CATCODES"][4]: #New line
                        thing[groupLevel][1] += i
                        curSpacer += i
                        line += 1

                    elif i in self.__options["CATCODES"][1]: #Start Group
                        statementMode = True
                        groupLevel += 1
                        if len(thing[groupLevel]) != 1:
                            thing[groupLevel][1] = ''
                        self.__statements.append([curStatement,curSpacer])
                        curStatement = i
                        curSpacer = ''
                        thing[groupLevel][0] = i

                    elif i in self.__options["CATCODES"][2]: #End Group
                        statementMode = True
                        groupLevel -= 1
                        if len(thing[groupLevel]) != 1:
                            thing[groupLevel][1] = ''
                        if groupLevel < 0:
                            raise Exception(f"Closing brace without matching opening brace on line {line}")
                        else:
                            self.__statements.append([curStatement,curSpacer])
                            curStatement = i
                            curSpacer = ''
                            thing[groupLevel][0] = i

                    elif curCatCode == prevCatCode:
                        statementMode = True
                        if len(thing[groupLevel]) != 1:
                            thing[groupLevel][1] = ''
                        curStatement += i
                        thing[groupLevel][0] += i

                    else:
                        statementMode = True
                        if len(thing[groupLevel]) != 1:
                            thing[groupLevel][1] = ''
                        self.__statements.append([curStatement,curSpacer])
                        curStatement = i
                        curSpacer = ''
                        thing[groupLevel][0] = i




                    print(thing[groupLevel][0])
                    try:
                        print(thing[groupLevel][1])
                    except:
                        pass

                print(i)
                print(self.__statements)
                print(statementMode)
                print(f"X{curSpacer}X")

        parseStatement(self,self.fileContents)

