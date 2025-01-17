#!/usr/bin/env python3
import io
import os
import queue
import uuid


class Code:
    def __init__(self, outFile):
        self.outFile = outFile
        self.counter = 0
        self.vmFileName = None
        self.labelCounter = 0

    # DONE
    def close(self):
        self.outFile.close()

    # DONE
    def updateVmFileName(self, name):
        self.vmFileName = os.path.basename(name).split(".")[0]

    # DONE
    def commandsToFile(self, commands):
        for line in commands:
            self.outFile.write(f"{line}\n")

    # DONE
    def getUniqLabel(self):
        return self.vmFileName + str(self.labelCounter)

    # DONE
    def updateUniqLabel(self):
        self.labelCounter = self.labelCounter + 1

    # DONE
    def writeHead(self, command):
        self.counter = self.counter + 1
        return ";; " + command + " - " + str(self.counter)

    # DONE
    def writeInit(self, bootstrap, isDir):
        commands = []

        if bootstrap or isDir:
            commands.append(self.writeHead("init"))

        if bootstrap:
            commands.append("leaw $256,%A")
            commands.append("movw %A,%D")
            commands.append("leaw $SP,%A")
            commands.append("movw %D,(%A)")

        if isDir:
            commands.append("leaw $Main.main, %A")
            commands.append("jmp")
            commands.append("nop")

        if bootstrap or isDir:
            self.commandsToFile(commands)

    def writeLabel(self, label):
        commands = []
        commands.append(self.writeHead("label") + " " + label)
        commands.append(f"{label}:")
        
        self.commandsToFile(commands)

    def writeGoto(self, label):
        commands = []
        commands.append(self.writeHead("goto") + " " + label)
        commands.append(f"leaw ${label}, %A")
        commands.append("jmp")
        commands.append("nop")

        self.commandsToFile(commands)
        
    def writeIf(self, label):
        commands = []
        commands.append(self.writeHead("if") + " " + label)
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("decw %D")
        commands.append("movw %D, (%A)")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("movw (%A), %D")
        commands.append(f"leaw ${label}, %A")
        commands.append("jl %D")
        commands.append("nop")

        self.commandsToFile(commands)


    # TODO
    def writeArithmetic(self, command):
        self.updateUniqLabel()
        if len(command) < 2:
            print("instrucão invalida {}".format(command))
        commands = []
        commands.append(self.writeHead(command))

        if command == "add":
            commands = self.operations(commands,"add")

        elif command == "sub":
            commands = self.operations(commands,"sub")

        elif command == "or":
            commands = self.operations(commands,"or")

        elif command == "and":
            commands = self.operations(commands,"and")

        elif command == "not":
           commands = self.operations1(commands,'not')

        elif command == "neg":
            commands = self.operations1(commands,'neg')

        elif command == "eq":
            # dica, usar self.getUniqLabel() para obter um label único
            commands = self.jump(commands,'je')

        elif command == "gt":
            # dica, usar self.getUniqLabel() para obter um label único
            commands = self.jump(commands,'jg')

        elif command == "lt":
            # dica, usar self.getUniqLabel() para obter um label único
            commands = self.jump(commands,'jl')

        self.commandsToFile(commands)

    #TODO
    def writePop(self, command, segment, index):
        self.updateUniqLabel()
        commands = []
        commands.append(self.writeHead(command) + " " + segment + " " + str(index))

        if segment == "" or segment == "constant":
            return False
        
        elif segment == "local":
            commands = self.wpop(commands,index,32)
        elif segment == "this":
            commands = self.wpop(commands,index,1024)
        elif segment == "that":
            commands = self.wpop(commands,index,1024)
        elif segment == "temp":
            commands = self.wpop(commands,index,5)
        elif segment == "pointer":
            commands = self.wpop(commands,index,3)
        elif segment == "static":
            pass
        elif segment == "argument":
            pass

        self.commandsToFile(commands)

    def writePush(self, command, segment, index):
        commands = []
        commands.append(self.writeHead(command + " " + segment + " " + str(index)))

        if segment == "constant":
            commands = self.wpushconstant(commands,index)
        elif segment == "local":
            commands = self.wpush(commands,index,1)
        elif segment == "argument":
            commands = self.wpush(commands,index,2)
        elif segment == "this":
            commands = self.wpush(commands,index,3)
        elif segment == "that":
            commands = self.wpush(commands,index,4)
        elif segment == "temp":
            commands = self.wpush1(commands,index,5)
        elif segment == "pointer":
            commands = self.wpush1(commands,index,3)
        elif segment == "static":
            pass

        self.commandsToFile(commands)

    # TODO
    def writeCall(self, funcName, numArgs):
        commands = []
        commands.append(self.writeHead("call") + " " + funcName + " " + str(numArgs))

        # TODO
        # ...

        self.commandsToFile(commands)

    # TODO
    def writeReturn(self):
        commands = []
        commands.append(self.writeHead("return"))

        # TODO
        # ...

        self.commandsToFile(commands)

    # TODO
    def writeFunction(self, funcName, numLocals):
        commands = []
        commands.append(self.writeHead("func") + " " + funcName + " " + str(numLocals))

        # TODO
        # ...

        self.commandsToFile(commands)
    
    

    def operations(self,commands,ope):
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("decw %D")
        commands.append("movw %D, (%A)")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("movw (%A), %D")
        commands.append("leaw $5, %A")
        commands.append("movw %D, (%A)")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("decw %A")
        commands.append("movw (%A), %A")
        commands.append("movw %A, %D")
        commands.append("leaw $5, %A")
        commands.append("movw (%A), %A")
        commands.append(f"{ope}w %D, %A, %D")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("decw %A")
        commands.append("movw %D, (%A)")
        return commands
    
    def operations1(self,commands,ope):
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("decw %D")
        commands.append("movw %D, %A")

        commands.append("movw (%A), %D")
        commands.append(f"{ope}w %D")

        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("decw %A")
        commands.append("movw %D, (%A)")
        return commands

    def jump(self,commands,jmp):
        if_true = self.getUniqLabel()
        true = 65535
        false = 0
        self.labelCounter +=1 
        end = self.getUniqLabel()

        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("decw %D")
        commands.append("movw %D, (%A)")

        commands.append("movw (%A), %A")
        commands.append("movw (%A), %D")
        commands.append("decw %A")
        commands.append("movw (%A), %A")
        commands.append("subw %A, %D, %D")
        commands.append(f"leaw ${if_true}, %A")
        commands.append(f"{jmp} %D")
        commands.append("nop")

        commands.append(f"leaw ${false}, %A")
        commands.append("movw %A, %D")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("decw %A")
        commands.append("movw %D, (%A)")
        commands.append(f"leaw ${end}, %A")
        commands.append("jmp")
        commands.append("nop")

        commands.append(f"{if_true}:")
        commands.append(f"leaw ${true}, %A")
        commands.append("movw %A, %D")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("decw %A")
        commands.append("movw %D, (%A)")
        commands.append(f"{end}:")
        return commands

    def wpop(self,commands,index,ram):
        # dica: usar o argumento index (push local 1)
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("decw %D")
        commands.append("movw %D, (%A)")

        commands.append(f"leaw ${ram}, %A")
        commands.append("movw %A, %D")
        commands.append(f"leaw ${index}, %A")
        commands.append("addw %A, %D, %D")

        commands.append("leaw $5, %A")
        commands.append("movw %D, (%A)")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("movw (%A), %D")
        commands.append("leaw $5, %A")
        commands.append("movw (%A), %A")
        commands.append("movw %D, (%A)")
        return commands

    def wpush(self,commands,index,ram):
        commands.append(f"leaw ${ram}, %A")
        commands.append("movw (%A), %D")
        commands.append(f"leaw ${index}, %A")
        commands.append("addw %A, %D, %D")
        commands.append(f"leaw ${ram}, %A")
        commands.append("movw %D, (%A)")

        commands.append("movw (%A), %A")
        commands.append("movw (%A), %D")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("movw %D, (%A)")

        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("incw %D")
        commands.append("movw %D, (%A)")
        return commands
    
    def wpush1(self,commands,index,ram):
        commands.append(f"leaw ${ram}, $A")
        commands.append("movw %A, %D")
        commands.append(f"leaw ${index}, %A")
        commands.append("addw %A, %D, %A")
        commands.append("movw (%A), %D")
        commands.append("leaw $SP, $A")
        commands.append("movw (%A), %A")
        commands.append("movw %D, (%A)")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("incw %D")
        commands.append("movw %D, (%A)")
        return commands
    
    def wpushconstant(self,commands,index):
        # dica: usar index para saber o valor da consante
        # push constant index
        commands.append(f"leaw ${index}, %A")
        commands.append("movw %A, %D")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %A")
        commands.append("movw %D, (%A)")
        commands.append("leaw $SP, %A")
        commands.append("movw (%A), %D")
        commands.append("incw %D")
        commands.append("movw %D, (%A)")
        return commands