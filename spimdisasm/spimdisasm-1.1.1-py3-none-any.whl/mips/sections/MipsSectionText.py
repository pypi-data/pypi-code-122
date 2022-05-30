#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

from ... import common

from .. import instructions
from .. import symbols

from ..MipsFileBase import FileBase

from . import SectionBase


class SectionText(SectionBase):
    def __init__(self, context: common.Context, vromStart: int, vromEnd: int, vram: int, filename: str, array_of_bytes: bytearray, segmentVromStart: int, overlayCategory: str|None):
        super().__init__(context, vromStart, vromEnd, vram, filename, array_of_bytes, common.FileSectionType.Text, segmentVromStart, overlayCategory)

        # TODO: do something with this information
        self.fileBoundaries: list[int] = list()

    @property
    def nFuncs(self) -> int:
        return len(self.symbolList)

    @staticmethod
    def wordListToInstructions(wordList: list[int], currentVram: int|None, isRsp: bool=False) -> list[instructions.InstructionBase]:
        instrsList: list[instructions.InstructionBase] = list()
        for word in wordList:
            if isRsp:
                instr = instructions.wordToInstructionRsp(word)
            else:
                instr = instructions.wordToInstruction(word)

            if currentVram is not None:
                instr.vram = currentVram
                currentVram += 4

            instrsList.append(instr)
        return instrsList

    def analyze(self):
        functionEnded = False
        farthestBranch = 0
        funcsStartsList = [0]
        unimplementedInstructionsFuncList = []

        instrsList = self.wordListToInstructions(self.words, self.getVramOffset(0), self.isRsp)

        instructionOffset = 0
        currentInstructionStart = 0
        currentFunctionSym = self.getSymbol(self.getVramOffset(instructionOffset), tryPlusOffset=False)

        isLikelyHandwritten = self.isHandwritten

        isInstrImplemented = True
        index = 0
        nInstr = len(instrsList)
        while index < nInstr:
            instr = instrsList[index]
            if not instr.isImplemented():
                isInstrImplemented = False

            if functionEnded:
                functionEnded = False

                isLikelyHandwritten = self.isHandwritten
                index += 1
                instructionOffset += 4
                isboundary = False
                # Loop over until we find a instruction that isn't a nop
                while index < nInstr:
                    instr = instrsList[index]
                    if instr.uniqueId != instructions.InstructionId.NOP:
                        if isboundary:
                            self.fileBoundaries.append(self.inFileOffset + index*4)
                        break
                    index += 1
                    instructionOffset += 4
                    isboundary = True

                currentInstructionStart = instructionOffset
                currentFunctionSym = self.getSymbol(self.getVramOffset(instructionOffset), tryPlusOffset=False)

                funcsStartsList.append(index)
                unimplementedInstructionsFuncList.append(not isInstrImplemented)
                if index >= len(instrsList):
                    break
                instr = instrsList[index]
                isInstrImplemented = instr.isImplemented()

            currentVram = self.getVramOffset(instructionOffset)

            if not self.isRsp and not isLikelyHandwritten:
                isLikelyHandwritten = instr.isLikelyHandwritten()

            if instr.isBranch() or instr.isUnconditionalBranch():
                if instr.uniqueId == instructions.InstructionId.J:
                    branch = instr.getInstrIndexAsVram() - currentVram
                else:
                    branch = instr.getBranchOffset()
                if branch > farthestBranch:
                    # keep track of the farthest branch target
                    farthestBranch = branch
                if branch < 0:
                    if branch + instructionOffset < 0:
                        # Whatever we are reading is not a valid instruction
                        break
                    # make sure to not branch outside of the current function
                    if not isLikelyHandwritten:
                        j = len(funcsStartsList) - 1
                        while j >= 0:
                            if (branch + instructionOffset) < funcsStartsList[j] * 4:
                                vram = self.getVramOffset(funcsStartsList[j]*4)
                                funcSymbol = self.getSymbol(vram, tryPlusOffset=False)
                                if funcSymbol is not None and funcSymbol.isTrustableFunction(self.isRsp):
                                    j -= 1
                                    continue
                                del funcsStartsList[j]
                                del unimplementedInstructionsFuncList[j-1]
                            else:
                                break
                            j -= 1

            elif instr.isJType():
                target = instr.getInstrIndexAsVram()
                if not self.isRsp:
                    if target >= 0x84000000:
                        # RSP address space?
                        isLikelyHandwritten = True
                self.addFunction(target, isAutogenerated=True)

            if not (farthestBranch > 0):
                if instr.uniqueId == instructions.InstructionId.JR:
                    if instr.rs == 31: # $ra
                        functionEnded = True
                elif instr.uniqueId == instructions.InstructionId.J:
                    if isLikelyHandwritten or self.isRsp:
                        functionEnded = True

            funcSymbol = self.getSymbol(currentVram + 8, tryPlusOffset=False)
            if funcSymbol is not None and funcSymbol.isTrustableFunction(self.isRsp):
                functionEnded = True

            if currentFunctionSym is not None and currentFunctionSym.size is not None:
                if instructionOffset + 8 == currentInstructionStart + currentFunctionSym.getSize():
                    functionEnded = True

            index += 1
            farthestBranch -= 4
            instructionOffset += 4

        unimplementedInstructionsFuncList.append(not isInstrImplemented)

        i = 0
        startsCount = len(funcsStartsList)
        for startIndex in range(startsCount):
            start = funcsStartsList[startIndex]
            hasUnimplementedIntrs = unimplementedInstructionsFuncList[startIndex]
            end = nInstr
            if startIndex + 1 < startsCount:
                end = funcsStartsList[startIndex+1]

            if start >= end:
                break

            # TODO: wire up back
            # funcName = f"func_{i}"
            # if len(self.context.offsetSymbols[self.sectionType]) > 0:
            #     possibleFuncName = self.context.getOffsetSymbol(start*4, self.sectionType)
            #     if possibleFuncName is not None:
            #         funcName = possibleFuncName.getName()

            localOffset = start*4
            vram = self.getVramOffset(localOffset)

            if common.GlobalConfig.DISASSEMBLE_UNKNOWN_INSTRUCTIONS or not hasUnimplementedIntrs:
                funcSymbol = self.addFunction(vram, isAutogenerated=True)
            elif common.GlobalConfig.ADD_NEW_SYMBOLS:
                self.addSymbol(vram, sectionType=self.sectionType, isAutogenerated=True)

            vrom = self.getVromOffset(localOffset)
            vromEnd = vrom + (end - start)*4
            func = symbols.SymbolFunction(self.context, vrom, vromEnd, self.inFileOffset + localOffset, vram, instrsList[start:end], self.segmentVromStart, self.overlayCategory)
            func.setCommentOffset(self.commentOffset)
            func.index = i
            func.pointersOffsets |= self.pointersOffsets
            func.hasUnimplementedIntrs = hasUnimplementedIntrs
            func.parent = self
            func.isRsp = self.isRsp
            func.analyze()
            self.symbolList.append(func)
            i += 1

    def printAnalyzisResults(self):
        super().printAnalyzisResults()
        if not common.GlobalConfig.PRINT_NEW_FILE_BOUNDARIES:
            return

        nBoundaries = len(self.fileBoundaries)
        if nBoundaries > 0:
            print(f"File {self.name}")
            print(f"Found {self.nFuncs} functions.")
            print(f"Found {nBoundaries} file boundaries.")

            print("\t offset, size, vram\t functions")

            for i in range(len(self.fileBoundaries)-1):
                start = self.fileBoundaries[i]
                end = self.fileBoundaries[i+1]

                functionsInBoundary = 0
                for func in self.symbolList:
                    funcOffset = func.inFileOffset - self.inFileOffset
                    if start <= funcOffset < end:
                        functionsInBoundary += 1
                fileVram = start + self.vram
                print("\t", f"{start+self.commentOffset:06X}", f"{end-start:04X}", f"{fileVram:08X}", "\t functions:", functionsInBoundary)

            start = self.fileBoundaries[-1]
            end = self.sizew*4 + self.inFileOffset

            functionsInBoundary = 0
            for func in self.symbolList:
                funcOffset = func.vram - self.vram
                if start <= funcOffset < end:
                    functionsInBoundary += 1
            fileVram = start + self.vram
            print("\t", f"{start+self.commentOffset:06X}", f"{end-start:04X}", f"{fileVram:08X}", "\t functions:", functionsInBoundary)

            print()
        return


    def compareToFile(self, other: FileBase):
        result = super().compareToFile(other)

        if isinstance(other, SectionText):
            result["text"] = {
                "diff_opcode": self.countDiffOpcodes(other),
                "same_opcode_same_args": self.countSameOpcodeButDifferentArguments(other),
            }

        return result

    def countDiffOpcodes(self, other: SectionText) -> int:
        result = 0
        for i in range(min(self.nFuncs, other.nFuncs)):
            func = self.symbolList[i]
            other_func = other.symbolList[i]
            assert isinstance(func, symbols.SymbolFunction)
            assert isinstance(other_func, symbols.SymbolFunction)
            result += func.countDiffOpcodes(other_func)
        return result

    def countSameOpcodeButDifferentArguments(self, other: SectionText) -> int:
        result = 0
        for i in range(min(self.nFuncs, other.nFuncs)):
            func = self.symbolList[i]
            other_func = other.symbolList[i]
            assert isinstance(func, symbols.SymbolFunction)
            assert isinstance(other_func, symbols.SymbolFunction)
            result += func.countSameOpcodeButDifferentArguments(other_func)
        return result

    def blankOutDifferences(self, other_file: FileBase) -> bool:
        if not common.GlobalConfig.REMOVE_POINTERS:
            return False

        if not isinstance(other_file, SectionText):
            return False

        was_updated = False
        for i in range(min(self.nFuncs, other_file.nFuncs)):
            func = self.symbolList[i]
            other_func = other_file.symbolList[i]
            assert isinstance(func, symbols.SymbolFunction)
            assert isinstance(other_func, symbols.SymbolFunction)
            was_updated = func.blankOutDifferences(other_func) or was_updated

        return was_updated

    def removePointers(self) -> bool:
        if not common.GlobalConfig.REMOVE_POINTERS:
            return False

        was_updated = False
        for func in self.symbolList:
            assert isinstance(func, symbols.SymbolFunction)
            was_updated = func.removePointers() or was_updated

        return was_updated

    def removeTrailingNops(self) -> bool:
        was_updated = False

        if self.nFuncs > 0:
            func = self.symbolList[-1]
            assert isinstance(func, symbols.SymbolFunction)
            func.removeTrailingNops()
            was_updated = True

        return was_updated
