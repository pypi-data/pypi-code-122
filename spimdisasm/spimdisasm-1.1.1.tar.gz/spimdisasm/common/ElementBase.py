#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Generator

from .GlobalConfig import GlobalConfig
from .ContextSymbols import ContextSymbol
from .SymbolsSegment import SymbolsSegment
from .Context import Context
from .FileSectionType import FileSectionType


class ElementBase:
    """Represents the base class used for most file sections and symbols.
    """

    def __init__(self, context: Context, vromStart: int, vromEnd: int, inFileOffset: int, vram: int, name: str, words: list[int], sectionType: FileSectionType, segmentVromStart: int, overlayCategory: str|None):
        """Constructor

        Args:
            context (Context):
            vromStart (int): The VROM address of this element
            vromEnd (int): The end of this element's VROM address
            inFileOffset (int): The offset of this element relative to the start of its file. It is also used to generate the first column of the disassembled line comment
            vram (int): The VRAM address of this element
            name (str): The name of this element
            words (list[int]): A list of words (4 bytes) corresponding to this element
            sectionType (FileSectionType): The section type this element corresponds to
        """

        self.context: Context = context
        self.vromStart: int = vromStart
        self.vromEnd: int = vromEnd
        self.inFileOffset: int = inFileOffset
        self.vram: int = vram
        self.name: str = name
        self.words: list[int] = words
        self.sectionType: FileSectionType = sectionType

        self.commentOffset: int = 0
        "This value is added to the first column of the disassembled line comment, allowing to change this value without messing inFileOffset"

        self.index: int|None = None
        "The index of the current element inside its parent or `None` if the index is unknown"

        self.parent: ElementBase|None = None
        "For elements that are contained in other elements, like symbols inside of sections"

        self.overlayCategory: str|None = overlayCategory
        self.segmentVromStart: int = segmentVromStart


    @property
    def sizew(self) -> int:
        "The amount of words this element has"
        return len(self.words)

    @property
    def vramEnd(self) -> int:
        "The end of this element's VRAM"
        return self.vram + self.sizew * 4


    def setVram(self, vram: int):
        self.vram = vram

    def setCommentOffset(self, commentOffset: int):
        self.commentOffset = commentOffset

    def getVromOffset(self, localOffset: int) -> int:
        return self.vromStart + localOffset

    def getVramOffset(self, localOffset: int) -> int:
        return self.vram + localOffset


    def getLabelFromSymbol(self, sym: ContextSymbol|None) -> str:
        "Generates a glabel for the passed symbol, including an optional index value if it was set and it is enabled in the GlobalConfig"
        if sym is not None:
            label = sym.getSymbolLabel()
            if GlobalConfig.GLABEL_ASM_COUNT:
                if self.index is not None:
                    label += f" # {self.index}"
            label +=  GlobalConfig.LINE_ENDS
            return label
        return ""


    def analyze(self):
        """Scans the words of this element, gathering as much info as possible.

        This method should be called only once for each element.
        """
        pass


    def disassemble(self) -> str:
        """Produces a disassembly of this element.

        Elements assume the `analyze` method was already called at this point.

        This method can be called as many times as the user wants to.
        """
        return ""


    def getSegment(self) -> SymbolsSegment:
        if self.overlayCategory is not None:
            # If this element is part of an overlay segment

            # Check only for the segment associated to this vrom address in this category
            segmentsPerVrom = self.context.overlaySegments.get(self.overlayCategory, None)
            if segmentsPerVrom is not None:
                overlaySegment = segmentsPerVrom.get(self.segmentVromStart, None)
                if overlaySegment is not None:
                    return overlaySegment

        return self.context.globalSegment

    def getSegmentForVram(self, vram: int) -> SymbolsSegment:
        if self.overlayCategory is not None:
            # If this element is part of an overlay segment

            # Check only for the segment associated to this vrom address in this category
            segmentsPerVrom = self.context.overlaySegments.get(self.overlayCategory, None)
            if segmentsPerVrom is not None:
                overlaySegment = segmentsPerVrom.get(self.segmentVromStart, None)
                if overlaySegment is not None:
                    if overlaySegment.isVramInRange(vram):
                        return overlaySegment

        if self.context.globalSegment.isVramInRange(vram):
            return self.context.globalSegment
        return self.context.unknownSegment


    def getSymbol(self, vramAddress: int, tryPlusOffset: bool = True, checkUpperLimit: bool = True) -> ContextSymbol|None:
        "Searches symbol or a symbol with an addend if `tryPlusOffset` is True"

        if self.overlayCategory is not None:
            # If this element is part of an overlay segment

            # Check only for the segment associated to this vrom address in this category
            segmentsPerVrom = self.context.overlaySegments.get(self.overlayCategory, None)
            if segmentsPerVrom is not None:
                overlaySegment = segmentsPerVrom.get(self.segmentVromStart, None)
                if overlaySegment is not None:
                    # if overlaySegment.isVramInRange(vramAddress):
                    contextSym = overlaySegment.getSymbol(vramAddress, tryPlusOffset=tryPlusOffset, checkUpperLimit=checkUpperLimit)
                    if contextSym is not None:
                        return contextSym

            # If the vram was not part of that segment, then check for every other overlay category
            for overlayCategory, segmentsPerVrom in self.context.overlaySegments.items():
                if self.overlayCategory != overlayCategory:
                    for overlaySegment in segmentsPerVrom.values():
                        # if overlaySegment.isVramInRange(vramAddress):
                        contextSym = overlaySegment.getSymbol(vramAddress, tryPlusOffset=tryPlusOffset, checkUpperLimit=checkUpperLimit)
                        if contextSym is not None:
                            return contextSym

        # if self.context.globalSegment.isVramInRange(vramAddress):
        contextSym = self.context.globalSegment.getSymbol(vramAddress, tryPlusOffset=tryPlusOffset, checkUpperLimit=checkUpperLimit)
        if contextSym is not None:
            return contextSym
        return self.context.unknownSegment.getSymbol(vramAddress, tryPlusOffset=tryPlusOffset, checkUpperLimit=checkUpperLimit)


    def getSymbolsRangeIter(self, addressStart: int, addressEnd: int) -> Generator[ContextSymbol, None, None]:
        segment = self.getSegmentForVram(addressStart)
        return segment.getSymbolsRangeIter(addressStart, addressEnd)

    def getSymbolsRange(self, addressStart: int, addressEnd: int) -> list[ContextSymbol]:
        segment = self.getSegmentForVram(addressStart)
        return segment.getSymbolsRange(addressStart, addressEnd)


    def getConstant(self, constantValue: int) -> ContextSymbol|None:
        segment = self.getSegment()
        return segment.getConstant(constantValue)


    def addSymbol(self, vramAddress: int, sectionType: FileSectionType=FileSectionType.Unknown, isAutogenerated: bool=False) -> ContextSymbol:
        segment = self.getSegmentForVram(vramAddress)
        return segment.addSymbol(vramAddress, sectionType=sectionType, isAutogenerated=isAutogenerated)

    def addFunction(self, vramAddress: int, isAutogenerated: bool=False) -> ContextSymbol:
        segment = self.getSegmentForVram(vramAddress)
        return segment.addFunction(vramAddress, isAutogenerated=isAutogenerated)

    def addBranchLabel(self, vramAddress: int, isAutogenerated: bool=False) -> ContextSymbol:
        segment = self.getSegmentForVram(vramAddress)
        return segment.addBranchLabel(vramAddress, isAutogenerated=isAutogenerated)

    def addJumpTable(self, vramAddress: int, isAutogenerated: bool=False) -> ContextSymbol:
        segment = self.getSegmentForVram(vramAddress)
        return segment.addJumpTable(vramAddress, isAutogenerated=isAutogenerated)

    def addJumpTableLabel(self, vramAddress: int, isAutogenerated: bool=False) -> ContextSymbol:
        segment = self.getSegmentForVram(vramAddress)
        return segment.addJumpTableLabel(vramAddress, isAutogenerated=isAutogenerated)


    def addConstant(self, constantValue: int, name: str) -> ContextSymbol:
        segment = self.getSegment()
        return segment.addConstant(constantValue, name)


    def addPointerInDataReference(self, pointer: int) -> None:
        segment = self.getSegmentForVram(pointer)
        segment.addPointerInDataReference(pointer)

    def popPointerInDataReference(self, pointer: int) -> int|None:
        segment = self.getSegmentForVram(pointer)
        return segment.popPointerInDataReference(pointer)

    def getPointerInDataReferencesIter(self, low: int, high: int) -> Generator[int, None, None]:
        segment = self.getSegmentForVram(low)
        return segment.getPointerInDataReferencesIter(low, high)


    def getLoPatch(self, loInstrVram: int|None) -> int|None:
        if loInstrVram is None:
            return None
        segment = self.getSegmentForVram(loInstrVram)
        return segment.getLoPatch(loInstrVram)

    def canUseAddendsOnData(self) -> bool:
        segment = self.getSegmentForVram(self.vram)
        return self.vram in segment.dataSymbolsWithReferencesWithAddends

    def canUseConstantsOnData(self) -> bool:
        segment = self.getSegmentForVram(self.vram)
        return self.vram in segment.dataReferencingConstants
