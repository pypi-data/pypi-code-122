#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

import dataclasses
import enum

from .GlobalConfig import GlobalConfig
from .FileSectionType import FileSectionType


class SymbolSpecialType(enum.Enum):
    function        = enum.auto()
    branchlabel     = enum.auto()
    jumptable       = enum.auto()
    jumptablelabel  = enum.auto()
    hardwarereg     = enum.auto()
    constant        = enum.auto()


    def toStr(self) -> str:
        return "@" + self.name

    @staticmethod
    def fromStr(symTypeStr: str|None) -> SymbolSpecialType|None:
        if symTypeStr == "@function":
            return SymbolSpecialType.function
        if symTypeStr == "@branchlabel":
            return SymbolSpecialType.branchlabel
        if symTypeStr == "@jumptable":
            return SymbolSpecialType.jumptable
        if symTypeStr == "@jumptablelabel":
            return SymbolSpecialType.jumptablelabel
        if symTypeStr == "@hardwarereg":
            return SymbolSpecialType.hardwarereg
        if symTypeStr == "@constant":
            return SymbolSpecialType.constant
        return None


@dataclasses.dataclass
class ContextSymbol:
    address: int
    name: str|None = None
    size: int|None = None
    type: SymbolSpecialType|str|None = None

    vromAddress: int|None = None

    sectionType: FileSectionType = FileSectionType.Unknown

    isDefined: bool = False
    "This symbol exists in any of the analyzed sections"
    isUserDeclared: bool = False
    "Declared externally by the user, but it may have not been found yet"
    isAutogenerated: bool = False
    "This symbol was automatically generated by the disassembler"

    isMaybeString: bool = False

    referenceCounter: int = 0
    "How much this symbol is referenced by something else"

    isOverlay: bool = False


    @property
    def vram(self) -> int:
        return self.address

    def hasNoType(self) -> bool:
        return self.type is None or self.type == ""


    def isTrustableFunction(self, rsp: bool=False) -> bool:
        """Checks if the function symbol should be trusted based on the current disassembler settings"""
        if GlobalConfig.TRUST_USER_FUNCTIONS and self.isUserDeclared:
            return True

        if GlobalConfig.TRUST_JAL_FUNCTIONS and self.isAutogenerated:
            return True

        if rsp:
            return True

        if self.type == SymbolSpecialType.function:
            return True

        return False


    def isByte(self) -> bool:
        if not GlobalConfig.USE_DOT_BYTE:
            return False
        return self.type in ("u8", "s8")

    def isShort(self) -> bool:
        if not GlobalConfig.USE_DOT_SHORT:
            return False
        return self.type in ("u16", "s16")


    def isString(self) -> bool:
        if self.type == "char" or self.type == "char*":
            return True
        elif self.hasNoType(): # no type information, let's try to guess
            if GlobalConfig.STRING_GUESSER and self.isMaybeString:
                return True
        return False

    def isFloat(self) -> bool:
        return self.type in ("f32", "Vec3f")

    def isDouble(self) -> bool:
        return self.type == "f64"

    def isJumpTable(self) -> bool:
        return self.type == SymbolSpecialType.jumptable

    def isMaybeConstVariable(self) -> bool:
        if self.isFloat():
            return False
        if self.isDouble():
            return False
        elif self.isJumpTable():
            return False
        elif self.isString():
            return False
        return True


    def isStatic(self) -> bool:
        return self.getName().startswith(".")

    def isLateRodata(self) -> bool:
        # if self.referenceCounter > 1: return False # ?
        return self.isJumpTable() or self.isFloat() or self.isDouble()


    def getDefaultName(self) -> str:
        suffix = ""
        if self.isOverlay:
            suffix = "_"
            if self.vromAddress is not None:
                suffix += f"{self.vromAddress:06X}"

        if self.type is not None:
            if self.type == SymbolSpecialType.function:
                return f"func_{self.address:08X}{suffix}"
            if self.type == SymbolSpecialType.branchlabel:
                return f".L{self.address:08X}{suffix}"
            if self.type == SymbolSpecialType.jumptable:
                return f"jtbl_{self.address:08X}{suffix}"
            if self.type == SymbolSpecialType.jumptablelabel:
                return f"L{self.address:08X}{suffix}"

        if GlobalConfig.AUTOGENERATED_NAMES_BASED_ON_SECTION_TYPE:
            if self.sectionType == FileSectionType.Rodata:
                return f"R_{self.address:06X}{suffix}"
            if self.sectionType == FileSectionType.Bss:
                return f"B_{self.address:06X}{suffix}"

        return f"D_{self.address:06X}{suffix}"

    def getName(self) -> str:
        if self.name is None:
            return self.getDefaultName()
        return self.name

    def setNameIfUnset(self, name: str) -> bool:
        if self.name is None:
            self.type = name
            return True
        return False

    def getSize(self) -> int:
        if self.size is None:
            return 4
        return self.size

    def getVrom(self) -> int:
        if self.vromAddress is None:
            return 0
        return self.vromAddress

    def setSizeIfUnset(self, size: int) -> bool:
        if self.size is None:
            self.size = size
            return True
        return False

    def getType(self) -> str:
        if self.type is None:
            return ""
        if isinstance(self.type, SymbolSpecialType):
            return self.type.toStr()
        return self.type

    def setTypeIfUnset(self, varType: str) -> bool:
        if self.hasNoType():
            self.type = varType
            return True
        return False

    def getSymbolPlusOffset(self, address: int) -> str:
        if self.address == address:
            return self.getName()
        if self.address > address:
            return f"{self.getName()} - 0x{self.address - address:X}"
        return f"{self.getName()} + 0x{address - self.address:X}"

    def getSymbolLabel(self) -> str:
        label = ""
        if self.isStatic():
            label += "/* static variable */" + GlobalConfig.LINE_ENDS
        if self.sectionType == FileSectionType.Text:
            label += GlobalConfig.ASM_TEXT_LABEL
        else:
            label += GlobalConfig.ASM_DATA_LABEL
        label += " " + self.getName()
        return label


    def toCsv(self) -> str:
        return f"0x{self.address:06X},{self.name},{self.getName()},{self.getType()},0x{self.getSize():X},{self.getVrom():X},{self.sectionType.toStr()},{self.isDefined},{self.isUserDeclared},{self.isAutogenerated},{self.isMaybeString},{self.referenceCounter},{self.isOverlay}"


class ContextOffsetSymbol(ContextSymbol):
    def __init__(self, offset: int, name: str, sectionType: FileSectionType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = offset
        self.name = name
        self.sectionType = sectionType

    # Relative to the start of the section
    @property
    def offset(self) -> int:
        return self.address

    def getName(self) -> str:
        if self.name is None:
            return super().getName()
        if self.isStatic():
            return self.name[1:]
        return self.name


class ContextRelocSymbol(ContextSymbol):
    relocSection: FileSectionType
    relocType: int = -1 # Same number as the .elf specification

    def __init__(self, offset: int, name: str|None, relocSection: FileSectionType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = offset
        self.name = name
        self.relocSection = relocSection

    # Relative to the start of the section
    @property
    def offset(self) -> int:
        return self.address

    def getNamePlusOffset(self, offset: int) -> str:
        if offset == 0:
            return self.getName()
        if offset < 0:
            return f"{self.getName()} - 0x{-offset:X}"
        return f"{self.getName()} + 0x{offset:X}"

    def toCsv(self) -> str:
        return super().toCsv() + f",{self.relocSection.toStr()},{self.relocType}"
