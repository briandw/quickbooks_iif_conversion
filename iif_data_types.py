from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict
import locale

locale.setlocale(locale.LC_ALL, '')  # Use user's locale settings


class RowType(Enum):
    HDR = 'HDR'
    ACCNT = 'ACCNT'
    INVITEM = 'INVITEM'
    ENDGRP = 'ENDGRP'
    CLASS = 'CLASS'
    CTYPE = 'CTYPE'
    CUST = 'CUST'
    VTYPE = 'VTYPE'
    VEND = 'VEND'
    EMP = 'EMP'
    OTHERNAME = 'OTHERNAME'
    SHIPMETH = 'SHIPMETH'
    PAYMETH = 'PAYMETH'
    INVMEMO = 'INVMEMO'
    TERMS = 'TERMS'
    BUD = 'BUD'
    TODO = 'TODO'
    VEHICLE = 'VEHICLE'
    SALESREP = 'SALESREP'
    SALESTAXCODE = 'SALESTAXCODE'

def try_parse_int(value: Optional[str]) -> Optional[int]:
    try:
        return int(value.replace(',', '').replace('"', '')) if value else None
    except ValueError:
        return None

def try_parse_float(value: Optional[str]) -> Optional[float]:
    try:
        return float(value.replace(',', '').replace('"', '')) if value else None
    except ValueError:
        return None


@dataclass
class HDR:
    PROD: str
    VER: str
    REL: str
    IIFVER: Optional[int] = None
    DATE: Optional[str] = ''
    TIME: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'HDR':
        # Parse IIFVER and TIME as integers if possible
        IIFVER = try_parse_int(row.get('IIFVER'))
        TIME = try_parse_int(row.get('TIME'))

        # DATE can be kept as a string or parsed into a date object
        DATE = row.get('DATE', '')

        return cls(
            PROD=row.get('PROD', ''),
            VER=row.get('VER', ''),
            REL=row.get('REL', ''),
            IIFVER=IIFVER,
            DATE=DATE,
            TIME=TIME,
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!HDR\tPROD\tVER\tREL\tIIFVER\tDATE\tTIME"

    def to_iif_row(self) -> str:
        return f"HDR\t{self.PROD}\t{self.VER}\t{self.REL}\t{self.IIFVER or ''}\t{self.DATE}\t{self.TIME or ''}"


@dataclass
class Account:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    ACCNTTYPE: str = ''
    OBAMOUNT: Optional[float] = None
    DESC: Optional[str] = ''
    ACCNUM: Optional[str] = ''
    SCD: Optional[int] = None
    EXTRA: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Account':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            ACCNTTYPE=row.get('ACCNTTYPE', ''),
            OBAMOUNT=try_parse_float(row.get('OBAMOUNT')),
            DESC=row.get('DESC', ''),
            ACCNUM=row.get('ACCNUM', ''),
            SCD=try_parse_int(row.get('SCD')),
            EXTRA=row.get('EXTRA', ''),
        )
    
    def OBAMOUNT_string(self) -> str:
        if self.OBAMOUNT is None:
            return '0.00'
        formatted = locale.format_string("%.2f", self.OBAMOUNT, grouping=True)
        return f'"{formatted}"' if abs(self.OBAMOUNT) >= 1000 else formatted

    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!ACCNT\tNAME\tREFNUM\tTIMESTAMP\tACCNTTYPE\tOBAMOUNT\tDESC\tACCNUM\tSCD\tEXTRA"

    def to_iif_row(self) -> str:
        return (
            f"ACCNT\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.ACCNTTYPE}\t"
            f"{self.OBAMOUNT_string()}\t{self.DESC or ''}\t{self.ACCNUM or ''}\t{self.SCD or 0}\t{self.EXTRA or ''}"
        )


@dataclass
class InventoryItem:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    INVITEMTYPE: str = ''
    DESC: Optional[str] = ''
    PURCHASEDESC: Optional[str] = ''
    ACCNT: Optional[str] = ''
    ASSETACCNT: Optional[str] = ''
    COGSACCNT: Optional[str] = ''
    PRICE: Optional[str] = ''
    COST: Optional[str] = ''
    TAXABLE: Optional[str] = ''
    SALESTAXCODE: Optional[str] = ''
    PAYMETH: Optional[str] = ''
    TAXVEND: Optional[str] = ''
    TAXDIST: Optional[str] = ''
    PREFVEND: Optional[str] = ''
    REORDERPOINT: Optional[str] = ''
    EXTRA: Optional[str] = ''
    CUSTFLD1: Optional[str] = ''
    CUSTFLD2: Optional[str] = ''
    CUSTFLD3: Optional[str] = ''
    CUSTFLD4: Optional[str] = ''
    CUSTFLD5: Optional[str] = ''
    DEP_TYPE: Optional[str] = ''
    ISPASSEDTHRU: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'InventoryItem':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            INVITEMTYPE=row.get('INVITEMTYPE', ''),
            DESC=row.get('DESC', ''),
            PURCHASEDESC=row.get('PURCHASEDESC', ''),
            ACCNT=row.get('ACCNT', ''),
            ASSETACCNT=row.get('ASSETACCNT', ''),
            COGSACCNT=row.get('COGSACCNT', ''),
            PRICE=row.get('PRICE', ''),
            COST=row.get('COST', ''),
            TAXABLE=row.get('TAXABLE', ''),
            SALESTAXCODE=row.get('SALESTAXCODE', ''),
            PAYMETH=row.get('PAYMETH', ''),
            TAXVEND=row.get('TAXVEND', ''),
            TAXDIST=row.get('TAXDIST', ''),
            PREFVEND=row.get('PREFVEND', ''),
            REORDERPOINT=row.get('REORDERPOINT', ''),
            EXTRA=row.get('EXTRA', ''),
            CUSTFLD1=row.get('CUSTFLD1', ''),
            CUSTFLD2=row.get('CUSTFLD2', ''),
            CUSTFLD3=row.get('CUSTFLD3', ''),
            CUSTFLD4=row.get('CUSTFLD4', ''),
            CUSTFLD5=row.get('CUSTFLD5', ''),
            DEP_TYPE=row.get('DEP_TYPE', ''),
            ISPASSEDTHRU=row.get('ISPASSEDTHRU', ''),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return (
            "!INVITEM\tNAME\tREFNUM\tTIMESTAMP\tINVITEMTYPE\tDESC\tPURCHASEDESC\tACCNT\tASSETACCNT\tCOGSACCNT\t"
            "PRICE\tCOST\tTAXABLE\tSALESTAXCODE\tPAYMETH\tTAXVEND\tTAXDIST\tPREFVEND\tREORDERPOINT\tEXTRA\t"
            "CUSTFLD1\tCUSTFLD2\tCUSTFLD3\tCUSTFLD4\tCUSTFLD5\tDEP_TYPE\tISPASSEDTHRU"
        )

    def to_iif_row(self) -> str:
        return (
            f"INVITEM\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.INVITEMTYPE}\t{self.DESC or ''}\t"
            f"{self.PURCHASEDESC or ''}\t{self.ACCNT or ''}\t{self.ASSETACCNT or ''}\t{self.COGSACCNT or ''}\t"
            f"{self.PRICE or ''}\t{self.COST or ''}\t{self.TAXABLE or ''}\t{self.SALESTAXCODE or ''}\t{self.PAYMETH or ''}\t"
            f"{self.TAXVEND or ''}\t{self.TAXDIST or ''}\t{self.PREFVEND or ''}\t{self.REORDERPOINT or ''}\t{self.EXTRA or ''}\t"
            f"{self.CUSTFLD1 or ''}\t{self.CUSTFLD2 or ''}\t{self.CUSTFLD3 or ''}\t{self.CUSTFLD4 or ''}\t{self.CUSTFLD5 or ''}\t"
            f"{self.DEP_TYPE or ''}\t{self.ISPASSEDTHRU or ''}"
        )

@dataclass
class OtherName:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    BADDR1: Optional[str] = ''
    BADDR2: Optional[str] = ''
    BADDR3: Optional[str] = ''
    BADDR4: Optional[str] = ''
    BADDR5: Optional[str] = ''
    PHONE1: Optional[str] = ''
    PHONE2: Optional[str] = ''
    FAXNUM: Optional[str] = ''
    EMAIL: Optional[str] = ''
    CONT1: Optional[str] = ''
    NOTEPAD: Optional[str] = ''
    SALUTATION: Optional[str] = ''
    COMPANYNAME: Optional[str] = ''
    FIRSTNAME: Optional[str] = ''
    MIDINIT: Optional[str] = ''
    LASTNAME: Optional[str] = ''

    @classmethod
    def from_row(cls, row: dict[str, str]) -> 'OtherName':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            BADDR1=row.get('BADDR1', ''),
            BADDR2=row.get('BADDR2', ''),
            BADDR3=row.get('BADDR3', ''),
            BADDR4=row.get('BADDR4', ''),
            BADDR5=row.get('BADDR5', ''),
            PHONE1=row.get('PHONE1', ''),
            PHONE2=row.get('PHONE2', ''),
            FAXNUM=row.get('FAXNUM', ''),
            EMAIL=row.get('EMAIL', ''),
            CONT1=row.get('CONT1', ''),
            NOTEPAD=row.get('NOTEPAD', ''),
            SALUTATION=row.get('SALUTATION', ''),
            COMPANYNAME=row.get('COMPANYNAME', ''),
            FIRSTNAME=row.get('FIRSTNAME', ''),
            MIDINIT=row.get('MIDINIT', ''),
            LASTNAME=row.get('LASTNAME', ''),
        )

    @classmethod
    def to_iif_header(cls) -> str:
        return (
            "!OTHERNAME\tNAME\tREFNUM\tTIMESTAMP\tBADDR1\tBADDR2\tBADDR3\tBADDR4\tBADDR5\t"
            "PHONE1\tPHONE2\tFAXNUM\tEMAIL\tCONT1\tNOTEPAD\tSALUTATION\tCOMPANYNAME\tFIRSTNAME\tMIDINIT\tLASTNAME"
        )

    def to_iif_row(self) -> str:
        return (
            f"OTHERNAME\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.BADDR1 or ''}\t"
            f"{self.BADDR2 or ''}\t{self.BADDR3 or ''}\t{self.BADDR4 or ''}\t{self.BADDR5 or ''}\t"
            f"{self.PHONE1 or ''}\t{self.PHONE2 or ''}\t{self.FAXNUM or ''}\t{self.EMAIL or ''}\t"
            f"{self.CONT1 or ''}\t{self.NOTEPAD or ''}\t{self.SALUTATION or ''}\t"
            f"{self.COMPANYNAME or ''}\t{self.FIRSTNAME or ''}\t{self.MIDINIT or ''}\t{self.LASTNAME or ''}"
        )

@dataclass
class EndGroup:
    @classmethod
    def to_iif_header(cls) -> str:
        return "!ENDGRP"
        
    def to_iif_row(self) -> str:
        return "ENDGRP"
    
@dataclass
class CustomerType:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'CustomerType':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!CTYPE\tNAME\tREFNUM\tTIMESTAMP"

    def to_iif_row(self) -> str:
        return f"CTYPE\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}"

@dataclass
class Vendor:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    PRINTAS: Optional[str] = ''
    ADDR1: Optional[str] = ''
    ADDR2: Optional[str] = ''
    ADDR3: Optional[str] = ''
    ADDR4: Optional[str] = ''
    ADDR5: Optional[str] = ''
    VTYPE: Optional[str] = ''
    CONT1: Optional[str] = ''
    CONT2: Optional[str] = ''
    PHONE1: Optional[str] = ''
    PHONE2: Optional[str] = ''
    FAXNUM: Optional[str] = ''
    EMAIL: Optional[str] = ''
    NOTE: Optional[str] = ''
    TAXID: Optional[str] = ''
    LIMIT: Optional[str] = ''
    TERMS: Optional[str] = ''
    NOTEPAD: Optional[str] = ''
    SALUTATION: Optional[str] = ''
    COMPANYNAME: Optional[str] = ''
    FIRSTNAME: Optional[str] = ''
    MIDINIT: Optional[str] = ''
    LASTNAME: Optional[str] = ''
    CUSTFLD1: Optional[str] = ''
    CUSTFLD2: Optional[str] = ''
    CUSTFLD3: Optional[str] = ''
    CUSTFLD4: Optional[str] = ''
    CUSTFLD5: Optional[str] = ''
    CUSTFLD6: Optional[str] = ''
    CUSTFLD7: Optional[str] = ''
    CUSTFLD8: Optional[str] = ''
    CUSTFLD9: Optional[str] = ''
    CUSTFLD10: Optional[str] = ''
    CUSTFLD11: Optional[str] = ''
    CUSTFLD12: Optional[str] = ''
    CUSTFLD13: Optional[str] = ''
    CUSTFLD14: Optional[str] = ''
    CUSTFLD15: Optional[str] = ''
    _1099: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Vendor':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            PRINTAS=row.get('PRINTAS', ''),
            ADDR1=row.get('ADDR1', ''),
            ADDR2=row.get('ADDR2', ''),
            ADDR3=row.get('ADDR3', ''),
            ADDR4=row.get('ADDR4', ''),
            ADDR5=row.get('ADDR5', ''),
            VTYPE=row.get('VTYPE', ''),
            CONT1=row.get('CONT1', ''),
            CONT2=row.get('CONT2', ''),
            PHONE1=row.get('PHONE1', ''),
            PHONE2=row.get('PHONE2', ''),
            FAXNUM=row.get('FAXNUM', ''),
            EMAIL=row.get('EMAIL', ''),
            NOTE=row.get('NOTE', ''),
            TAXID=row.get('TAXID', ''),
            LIMIT=row.get('LIMIT', ''),
            TERMS=row.get('TERMS', ''),
            NOTEPAD=row.get('NOTEPAD', ''),
            SALUTATION=row.get('SALUTATION', ''),
            COMPANYNAME=row.get('COMPANYNAME', ''),
            FIRSTNAME=row.get('FIRSTNAME', ''),
            MIDINIT=row.get('MIDINIT', ''),
            LASTNAME=row.get('LASTNAME', ''),
            CUSTFLD1=row.get('CUSTFLD1', ''),
            CUSTFLD2=row.get('CUSTFLD2', ''),
            CUSTFLD3=row.get('CUSTFLD3', ''),
            CUSTFLD4=row.get('CUSTFLD4', ''),
            CUSTFLD5=row.get('CUSTFLD5', ''),
            CUSTFLD6=row.get('CUSTFLD6', ''),
            CUSTFLD7=row.get('CUSTFLD7', ''),
            CUSTFLD8=row.get('CUSTFLD8', ''),
            CUSTFLD9=row.get('CUSTFLD9', ''),
            CUSTFLD10=row.get('CUSTFLD10', ''),
            CUSTFLD11=row.get('CUSTFLD11', ''),
            CUSTFLD12=row.get('CUSTFLD12', ''),
            CUSTFLD13=row.get('CUSTFLD13', ''),
            CUSTFLD14=row.get('CUSTFLD14', ''),
            CUSTFLD15=row.get('CUSTFLD15', ''),
            _1099=row.get('1099', ''),
        )

    @classmethod
    def to_iif_header(cls) -> str:
        return (
            "!VEND\tNAME\tREFNUM\tTIMESTAMP\tPRINTAS\tADDR1\tADDR2\tADDR3\tADDR4\tADDR5\tVTYPE\tCONT1\tCONT2\tPHONE1\t"
            "PHONE2\tFAXNUM\tEMAIL\tNOTE\tTAXID\tLIMIT\tTERMS\tNOTEPAD\tSALUTATION\tCOMPANYNAME\tFIRSTNAME\tMIDINIT\t"
            "LASTNAME\tCUSTFLD1\tCUSTFLD2\tCUSTFLD3\tCUSTFLD4\tCUSTFLD5\tCUSTFLD6\tCUSTFLD7\tCUSTFLD8\tCUSTFLD9\tCUSTFLD10\t"
            "CUSTFLD11\tCUSTFLD12\tCUSTFLD13\tCUSTFLD14\tCUSTFLD15\t1099"
        )

    def to_iif_row(self) -> str:
        return (
            f"VEND\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.PRINTAS or ''}\t{self.ADDR1 or ''}\t"
            f"{self.ADDR2 or ''}\t{self.ADDR3 or ''}\t{self.ADDR4 or ''}\t{self.ADDR5 or ''}\t{self.VTYPE or ''}\t"
            f"{self.CONT1 or ''}\t{self.CONT2 or ''}\t{self.PHONE1 or ''}\t{self.PHONE2 or ''}\t{self.FAXNUM or ''}\t"
            f"{self.EMAIL or ''}\t{self.NOTE or ''}\t{self.TAXID or ''}\t{self.LIMIT or ''}\t{self.TERMS or ''}\t"
            f"{self.NOTEPAD or ''}\t{self.SALUTATION or ''}\t{self.COMPANYNAME or ''}\t{self.FIRSTNAME or ''}\t"
            f"{self.MIDINIT or ''}\t{self.LASTNAME or ''}\t{self.CUSTFLD1 or ''}\t{self.CUSTFLD2 or ''}\t"
            f"{self.CUSTFLD3 or ''}\t{self.CUSTFLD4 or ''}\t{self.CUSTFLD5 or ''}\t{self.CUSTFLD6 or ''}\t"
            f"{self.CUSTFLD7 or ''}\t{self.CUSTFLD8 or ''}\t{self.CUSTFLD9 or ''}\t{self.CUSTFLD10 or ''}\t"
            f"{self.CUSTFLD11 or ''}\t{self.CUSTFLD12 or ''}\t{self.CUSTFLD13 or ''}\t{self.CUSTFLD14 or ''}\t"
            f"{self.CUSTFLD15 or ''}\t{self._1099 or ''}"
        )

@dataclass
class Customer:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    BADDR1: Optional[str] = ''
    BADDR2: Optional[str] = ''
    BADDR3: Optional[str] = ''
    BADDR4: Optional[str] = ''
    BADDR5: Optional[str] = ''
    SADDR1: Optional[str] = ''
    SADDR2: Optional[str] = ''
    SADDR3: Optional[str] = ''
    SADDR4: Optional[str] = ''
    SADDR5: Optional[str] = ''
    PHONE1: Optional[str] = ''
    PHONE2: Optional[str] = ''
    FAXNUM: Optional[str] = ''
    EMAIL: Optional[str] = ''
    CONT1: Optional[str] = ''
    CONT2: Optional[str] = ''
    CTYPE: Optional[str] = ''
    TERMS: Optional[str] = ''
    TAXABLE: Optional[str] = ''
    SALESTAXCODE: Optional[str] = ''
    LIMIT: Optional[str] = ''
    RESALENUM: Optional[str] = ''
    REP: Optional[str] = ''
    TAXITEM: Optional[str] = ''
    NOTEPAD: Optional[str] = ''
    SALUTATION: Optional[str] = ''
    COMPANYNAME: Optional[str] = ''
    FIRSTNAME: Optional[str] = ''
    MIDINIT: Optional[str] = ''
    LASTNAME: Optional[str] = ''
    CUSTFLD1: Optional[str] = ''
    CUSTFLD2: Optional[str] = ''
    CUSTFLD3: Optional[str] = ''
    CUSTFLD4: Optional[str] = ''
    CUSTFLD5: Optional[str] = ''
    CUSTFLD6: Optional[str] = ''
    CUSTFLD7: Optional[str] = ''
    CUSTFLD8: Optional[str] = ''
    CUSTFLD9: Optional[str] = ''
    CUSTFLD10: Optional[str] = ''
    CUSTFLD11: Optional[str] = ''
    CUSTFLD12: Optional[str] = ''
    CUSTFLD13: Optional[str] = ''
    CUSTFLD14: Optional[str] = ''
    CUSTFLD15: Optional[str] = ''
    JOBDESC: Optional[str] = ''
    JOBTYPE: Optional[str] = ''
    JOBSTATUS: Optional[str] = ''
    JOBSTART: Optional[str] = ''
    JOBPROJEND: Optional[str] = ''
    JOBEND: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Customer':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            BADDR1=row.get('BADDR1', ''),
            BADDR2=row.get('BADDR2', ''),
            BADDR3=row.get('BADDR3', ''),
            BADDR4=row.get('BADDR4', ''),
            BADDR5=row.get('BADDR5', ''),
            SADDR1=row.get('SADDR1', ''),
            SADDR2=row.get('SADDR2', ''),
            SADDR3=row.get('SADDR3', ''),
            SADDR4=row.get('SADDR4', ''),
            SADDR5=row.get('SADDR5', ''),
            PHONE1=row.get('PHONE1', ''),
            PHONE2=row.get('PHONE2', ''),
            FAXNUM=row.get('FAXNUM', ''),
            EMAIL=row.get('EMAIL', ''),
            CONT1=row.get('CONT1', ''),
            CONT2=row.get('CONT2', ''),
            CTYPE=row.get('CTYPE', ''),
            TERMS=row.get('TERMS', ''),
            TAXABLE=row.get('TAXABLE', ''),
            SALESTAXCODE=row.get('SALESTAXCODE', ''),
            LIMIT=row.get('LIMIT', ''),
            RESALENUM=row.get('RESALENUM', ''),
            REP=row.get('REP', ''),
            TAXITEM=row.get('TAXITEM', ''),
            NOTEPAD=row.get('NOTEPAD', ''),
            SALUTATION=row.get('SALUTATION', ''),
            COMPANYNAME=row.get('COMPANYNAME', ''),
            FIRSTNAME=row.get('FIRSTNAME', ''),
            MIDINIT=row.get('MIDINIT', ''),
            LASTNAME=row.get('LASTNAME', ''),
            CUSTFLD1=row.get('CUSTFLD1', ''),
            CUSTFLD2=row.get('CUSTFLD2', ''),
            CUSTFLD3=row.get('CUSTFLD3', ''),
            CUSTFLD4=row.get('CUSTFLD4', ''),
            CUSTFLD5=row.get('CUSTFLD5', ''),
            CUSTFLD6=row.get('CUSTFLD6', ''),
            CUSTFLD7=row.get('CUSTFLD7', ''),
            CUSTFLD8=row.get('CUSTFLD8', ''),
            CUSTFLD9=row.get('CUSTFLD9', ''),
            CUSTFLD10=row.get('CUSTFLD10', ''),
            CUSTFLD11=row.get('CUSTFLD11', ''),
            CUSTFLD12=row.get('CUSTFLD12', ''),
            CUSTFLD13=row.get('CUSTFLD13', ''),
            CUSTFLD14=row.get('CUSTFLD14', ''),
            CUSTFLD15=row.get('CUSTFLD15', ''),
            JOBDESC=row.get('JOBDESC', ''),
            JOBTYPE=row.get('JOBTYPE', ''),
            JOBSTATUS=row.get('JOBSTATUS', ''),
            JOBSTART=row.get('JOBSTART', ''),
            JOBPROJEND=row.get('JOBPROJEND', ''),
            JOBEND=row.get('JOBEND', ''),
        )

    @classmethod
    def to_iif_header(cls) -> str:
        return (
            "!CUST\tNAME\tREFNUM\tTIMESTAMP\tBADDR1\tBADDR2\tBADDR3\tBADDR4\tBADDR5\tSADDR1\tSADDR2\tSADDR3\tSADDR4\tSADDR5\t"
            "PHONE1\tPHONE2\tFAXNUM\tEMAIL\tCONT1\tCONT2\tCTYPE\tTERMS\tTAXABLE\tSALESTAXCODE\tLIMIT\tRESALENUM\tREP\t"
            "TAXITEM\tNOTEPAD\tSALUTATION\tCOMPANYNAME\tFIRSTNAME\tMIDINIT\tLASTNAME\tCUSTFLD1\tCUSTFLD2\tCUSTFLD3\t"
            "CUSTFLD4\tCUSTFLD5\tCUSTFLD6\tCUSTFLD7\tCUSTFLD8\tCUSTFLD9\tCUSTFLD10\tCUSTFLD11\tCUSTFLD12\tCUSTFLD13\t"
            "CUSTFLD14\tCUSTFLD15\tJOBDESC\tJOBTYPE\tJOBSTATUS\tJOBSTART\tJOBPROJEND\tJOBEND"
        )

    def to_iif_row(self) -> str:
        return (
            f"CUST\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.BADDR1 or ''}\t{self.BADDR2 or ''}\t"
            f"{self.BADDR3 or ''}\t{self.BADDR4 or ''}\t{self.BADDR5 or ''}\t{self.SADDR1 or ''}\t{self.SADDR2 or ''}\t"
            f"{self.SADDR3 or ''}\t{self.SADDR4 or ''}\t{self.SADDR5 or ''}\t{self.PHONE1 or ''}\t{self.PHONE2 or ''}\t"
            f"{self.FAXNUM or ''}\t{self.EMAIL or ''}\t{self.CONT1 or ''}\t{self.CONT2 or ''}\t{self.CTYPE or ''}\t"
            f"{self.TERMS or ''}\t{self.TAXABLE or ''}\t{self.SALESTAXCODE or ''}\t{self.LIMIT or ''}\t"
            f"{self.RESALENUM or ''}\t{self.REP or ''}\t{self.TAXITEM or ''}\t{self.NOTEPAD or ''}\t"
            f"{self.SALUTATION or ''}\t{self.COMPANYNAME or ''}\t{self.FIRSTNAME or ''}\t{self.MIDINIT or ''}\t"
            f"{self.LASTNAME or ''}\t{self.CUSTFLD1 or ''}\t{self.CUSTFLD2 or ''}\t{self.CUSTFLD3 or ''}\t"
            f"{self.CUSTFLD4 or ''}\t{self.CUSTFLD5 or ''}\t{self.CUSTFLD6 or ''}\t{self.CUSTFLD7 or ''}\t"
            f"{self.CUSTFLD8 or ''}\t{self.CUSTFLD9 or ''}\t{self.CUSTFLD10 or ''}\t{self.CUSTFLD11 or ''}\t"
            f"{self.CUSTFLD12 or ''}\t{self.CUSTFLD13 or ''}\t{self.CUSTFLD14 or ''}\t{self.CUSTFLD15 or ''}\t"
            f"{self.JOBDESC or ''}\t{self.JOBTYPE or ''}\t{self.JOBSTATUS or ''}\t{self.JOBSTART or ''}\t"
            f"{self.JOBPROJEND or ''}\t{self.JOBEND or ''}"
        )


@dataclass
class ShippingMethod:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'ShippingMethod':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!SHIPMETH\tNAME\tREFNUM\tTIMESTAMP"

    def to_iif_row(self) -> str:
        return f"SHIPMETH\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}"
    
@dataclass
class PaymentMethod:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'PaymentMethod':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!PAYMETH\tNAME\tREFNUM\tTIMESTAMP"

    def to_iif_row(self) -> str:
        return f"PAYMETH\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}"

@dataclass
class InvoiceMemo:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None

    @classmethod
    def from_row(cls, row: dict[str, str]) -> 'InvoiceMemo':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
        )

    @classmethod
    def to_iif_header(cls) -> str:
        return "!INVMEMO\tNAME\tREFNUM\tTIMESTAMP"

    def to_iif_row(self) -> str:
        return f"INVMEMO\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}"
    
@dataclass
class Terms:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    DUEDAYS: Optional[int] = None
    MINDAYS: Optional[int] = None
    DISCPER: Optional[str] = ''
    DISCDAYS: Optional[int] = None
    TERMSTYPE: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Terms':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            DUEDAYS=try_parse_int(row.get('DUEDAYS')),
            MINDAYS=try_parse_int(row.get('MINDAYS')),
            DISCPER=row.get('DISCPER', ''),
            DISCDAYS=try_parse_int(row.get('DISCDAYS')),
            TERMSTYPE=try_parse_int(row.get('TERMSTYPE')),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!TERMS\tNAME\tREFNUM\tTIMESTAMP\tDUEDAYS\tMINDAYS\tDISCPER\tDISCDAYS\tTERMSTYPE"

    def to_iif_row(self) -> str:
        return (
            f"TERMS\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.DUEDAYS or 0}\t"
            f"{self.MINDAYS or 0}\t{self.DISCPER or ''}\t{self.DISCDAYS or 0}\t{self.TERMSTYPE or 0}"
        )

@dataclass
class SalesTaxCode:
    CODE: str
    REFNUM: Optional[int] = None
    HIDDEN: Optional[str] = ''
    DESC: Optional[str] = ''
    TAXABLE: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'SalesTaxCode':
        return cls(
            CODE=row.get('CODE', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            HIDDEN=row.get('HIDDEN', ''),
            DESC=row.get('DESC', ''),
            TAXABLE=row.get('TAXABLE', ''),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!SALESTAXCODE\tCODE\tREFNUM\tHIDDEN\tDESC\tTAXABLE"

    def to_iif_row(self) -> str:
        return f"SALESTAXCODE\t{self.CODE}\t{self.REFNUM or ''}\t{self.HIDDEN or ''}\t{self.DESC or ''}\t{self.TAXABLE or ''}"

@dataclass
class ClassRecord:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'ClassRecord':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!CLASS\tNAME\tREFNUM\tTIMESTAMP"

    def to_iif_row(self) -> str:
        return f"CLASS\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}"

@dataclass
class VendorType:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'VendorType':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!VTYPE\tNAME\tREFNUM\tTIMESTAMP"

    def to_iif_row(self) -> str:
        return f"VTYPE\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}"
    
@dataclass
class Employee:
    NAME: str
    REFNUM: Optional[int] = None
    TIMESTAMP: Optional[int] = None
    INIT: Optional[str] = ''
    ADDR1: Optional[str] = ''
    ADDR2: Optional[str] = ''
    ADDR3: Optional[str] = ''
    ADDR4: Optional[str] = ''
    ADDR5: Optional[str] = ''
    SSNO: Optional[str] = ''
    PHONE1: Optional[str] = ''
    PHONE2: Optional[str] = ''
    EMAIL: Optional[str] = ''
    NOTEPAD: Optional[str] = ''
    FIRSTNAME: Optional[str] = ''
    MIDINIT: Optional[str] = ''
    LASTNAME: Optional[str] = ''
    SALUTATION: Optional[str] = ''
    CUSTFLD1: Optional[str] = ''
    CUSTFLD2: Optional[str] = ''
    CUSTFLD3: Optional[str] = ''
    CUSTFLD4: Optional[str] = ''
    CUSTFLD5: Optional[str] = ''
    CUSTFLD6: Optional[str] = ''
    CUSTFLD7: Optional[str] = ''
    CUSTFLD8: Optional[str] = ''
    CUSTFLD9: Optional[str] = ''
    CUSTFLD10: Optional[str] = ''
    CUSTFLD11: Optional[str] = ''
    CUSTFLD12: Optional[str] = ''
    CUSTFLD13: Optional[str] = ''
    CUSTFLD14: Optional[str] = ''
    CUSTFLD15: Optional[str] = ''
    HIDDEN: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Employee':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            TIMESTAMP=try_parse_int(row.get('TIMESTAMP')),
            INIT=row.get('INIT', ''),
            ADDR1=row.get('ADDR1', ''),
            ADDR2=row.get('ADDR2', ''),
            ADDR3=row.get('ADDR3', ''),
            ADDR4=row.get('ADDR4', ''),
            ADDR5=row.get('ADDR5', ''),
            SSNO=row.get('SSNO', ''),
            PHONE1=row.get('PHONE1', ''),
            PHONE2=row.get('PHONE2', ''),
            EMAIL=row.get('EMAIL', ''),
            NOTEPAD=row.get('NOTEPAD', ''),
            FIRSTNAME=row.get('FIRSTNAME', ''),
            MIDINIT=row.get('MIDINIT', ''),
            LASTNAME=row.get('LASTNAME', ''),
            SALUTATION=row.get('SALUTATION', ''),
            CUSTFLD1=row.get('CUSTFLD1', ''),
            CUSTFLD2=row.get('CUSTFLD2', ''),
            CUSTFLD3=row.get('CUSTFLD3', ''),
            CUSTFLD4=row.get('CUSTFLD4', ''),
            CUSTFLD5=row.get('CUSTFLD5', ''),
            CUSTFLD6=row.get('CUSTFLD6', ''),
            CUSTFLD7=row.get('CUSTFLD7', ''),
            CUSTFLD8=row.get('CUSTFLD8', ''),
            CUSTFLD9=row.get('CUSTFLD9', ''),
            CUSTFLD10=row.get('CUSTFLD10', ''),
            CUSTFLD11=row.get('CUSTFLD11', ''),
            CUSTFLD12=row.get('CUSTFLD12', ''),
            CUSTFLD13=row.get('CUSTFLD13', ''),
            CUSTFLD14=row.get('CUSTFLD14', ''),
            CUSTFLD15=row.get('CUSTFLD15', ''),
            HIDDEN=row.get('HIDDEN', ''),
        )

    @classmethod
    def to_iif_header(cls) -> str:
        return ("!EMP\tNAME\tREFNUM\tTIMESTAMP\tINIT\tADDR1\tADDR2\tADDR3\tADDR4\tADDR5\t"
                "SSNO\tPHONE1\tPHONE2\tEMAIL\tNOTEPAD\tFIRSTNAME\tMIDINIT\tLASTNAME\tSALUTATION\t"
                "CUSTFLD1\tCUSTFLD2\tCUSTFLD3\tCUSTFLD4\tCUSTFLD5\tCUSTFLD6\tCUSTFLD7\tCUSTFLD8\t"
                "CUSTFLD9\tCUSTFLD10\tCUSTFLD11\tCUSTFLD12\tCUSTFLD13\tCUSTFLD14\tCUSTFLD15\tHIDDEN"
        )

    def to_iif_row(self) -> str:
        return (
            f"EMP\t{self.NAME}\t{self.REFNUM or ''}\t{self.TIMESTAMP or 0}\t{self.INIT or ''}\t"
            f"{self.ADDR1 or ''}\t{self.ADDR2 or ''}\t{self.ADDR3 or ''}\t{self.ADDR4 or ''}\t"
            f"{self.ADDR5 or ''}\t{self.SSNO or ''}\t{self.PHONE1 or ''}\t{self.PHONE2 or ''}\t"
            f"{self.EMAIL or ''}\t{self.NOTEPAD or ''}\t{self.FIRSTNAME or ''}\t{self.MIDINIT or ''}\t"
            f"{self.LASTNAME or ''}\t{self.SALUTATION or ''}\t"
            f"{self.CUSTFLD1 or ''}\t{self.CUSTFLD2 or ''}\t{self.CUSTFLD3 or ''}\t{self.CUSTFLD4 or ''}\t"
            f"{self.CUSTFLD5 or ''}\t{self.CUSTFLD6 or ''}\t{self.CUSTFLD7 or ''}\t{self.CUSTFLD8 or ''}\t"
            f"{self.CUSTFLD9 or ''}\t{self.CUSTFLD10 or ''}\t{self.CUSTFLD11 or ''}\t{self.CUSTFLD12 or ''}\t"
            f"{self.CUSTFLD13 or ''}\t{self.CUSTFLD14 or ''}\t{self.CUSTFLD15 or ''}\t{self.HIDDEN or ''}"
        )
    
@dataclass
class Budget:
    ACCNT: str
    PERIOD: Optional[str] = ''
    AMOUNTS: List[Optional[float]] = field(default_factory=list)
    STARTDATE: Optional[str] = ''
    CLASS: Optional[str] = ''
    CUSTOMER: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Budget':
        amounts = []
        # Assuming AMOUNT fields are named AMOUNT, AMOUNT, ..., need to adjust based on actual field names
        for i in range(1, 13):
            amount_field = f'AMOUNT{i}'
            amount = try_parse_float(row.get(amount_field))
            amounts.append(amount)
        return cls(
            ACCNT=row.get('ACCNT', ''),
            PERIOD=row.get('PERIOD', ''),
            AMOUNTS=amounts,
            STARTDATE=row.get('STARTDATE', ''),
            CLASS=row.get('CLASS', ''),
            CUSTOMER=row.get('CUSTOMER', ''),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return (
            "!BUD\tACCNT\tPERIOD\t" +
            "\t".join(f"AMOUNT" for i in range(1, 13)) +
            "\tSTARTDATE\tCLASS\tCUSTOMER"
        )

    def to_iif_row(self) -> str:
        return (
            f"BUD\t{self.ACCNT}\t{self.PERIOD or ''}\t" +
            "\t".join(str(amount or '') for amount in self.AMOUNTS) +
            f"\t{self.STARTDATE or ''}\t{self.CLASS or ''}\t{self.CUSTOMER or ''}"
        )
    
@dataclass
class ToDoItem:
    REFNUM: Optional[int] = None
    ISDONE: Optional[str] = ''
    DATE: Optional[str] = ''
    DESC: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'ToDoItem':
        return cls(
            REFNUM=try_parse_int(row.get('REFNUM')),
            ISDONE=row.get('ISDONE', ''),
            DATE=row.get('DATE', ''),
            DESC=row.get('DESC', ''),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!TODO\tREFNUM\tISDONE\tDATE\tDESC"

    def to_iif_row(self) -> str:
        return f"TODO\t{self.REFNUM or ''}\t{self.ISDONE or ''}\t{self.DATE or ''}\t{self.DESC or ''}"

@dataclass
class Vehicle:
    NAME: str
    REFNUM: Optional[int] = None
    DESC: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'Vehicle':
        return cls(
            NAME=row.get('NAME', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            DESC=row.get('DESC', ''),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!VEHICLE\tNAME\tREFNUM\tDESC"

    def to_iif_row(self) -> str:
        return f"VEHICLE\t{self.NAME}\t{self.REFNUM or ''}\t{self.DESC or ''}"
    
@dataclass
class SalesRep:
    INIT: Optional[str] = ''
    REFNUM: Optional[int] = None
    NAME: Optional[str] = ''
    TYPE: Optional[str] = ''

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> 'SalesRep':
        return cls(
            INIT=row.get('INIT', ''),
            REFNUM=try_parse_int(row.get('REFNUM')),
            NAME=row.get('NAME', ''),
            TYPE=row.get('TYPE', ''),
        )
    
    @classmethod
    def to_iif_header(cls) -> str:
        return "!SALESREP\tINIT\tREFNUM\tNAME\tTYPE"

    def to_iif_row(self) -> str:
        return (
            f"SALESREP\t{self.INIT or ''}\t{self.REFNUM or ''}\t{self.NAME or ''}\t{self.TYPE or ''}"
        )
    
def get_class_by_row_type(row_type: RowType):
    mapping = {
        RowType.HDR: HDR,
        RowType.ACCNT: Account,
        RowType.INVITEM: InventoryItem,
        RowType.CLASS: ClassRecord,
        RowType.VTYPE: VendorType,
        RowType.EMP: Employee,
        RowType.ENDGRP: EndGroup,
        RowType.BUD: Budget,
        RowType.TODO: ToDoItem,
        RowType.VEHICLE: Vehicle,
        RowType.SALESREP: SalesRep,
        RowType.CTYPE: CustomerType,
        RowType.CUST: Customer,
        RowType.VEND: Vendor,
        RowType.SHIPMETH: ShippingMethod,
        RowType.PAYMETH: PaymentMethod,
        RowType.TERMS: Terms,
        RowType.SALESTAXCODE: SalesTaxCode,
        RowType.OTHERNAME: OtherName,
        RowType.INVMEMO: InvoiceMemo
        # Add other mappings as needed
    }
    return mapping.get(row_type)

