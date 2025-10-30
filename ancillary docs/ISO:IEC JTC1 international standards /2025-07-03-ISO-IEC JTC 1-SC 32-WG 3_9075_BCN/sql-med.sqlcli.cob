
* The following COBOL library item (.cob) is a "digital artifact" that contains
* lines of code in the COBOL programming language in, for example, the WORKING-STORAGE
* section of application programs written in COBOL that use SQL-implementations. 
*
* A typical inclusion is:
*
*    COPY SQLCLI.
*

    * DATALINK ATTRIBUTES
    01 SQL-ATTR-DL-URL-COMPLETE             PIC S9(4) BINARY VALUE IS     3.
    01 SQL-ATTR-DL-URL-PATH                 PIC S9(4) BINARY VALUE IS     4.
    01 SQL-ATTR-DL-URL-PATH-ONLY            PIC S9(4) BINARY VALUE IS     5.
    01 SQL-ATTR-DL-URL-SCHEME               PIC S9(4) BINARY VALUE IS     6.
    01 SQL-ATTR-DL-URL-SERVER               PIC S9(4) BINARY VALUE IS     7.

    01 SQL-DATALINK                         PIC S9(4) BINARY VALUE IS    70.

    01 SQL-API-SQLBUILDDATALINK             PIC S9(4) BINARY VALUE IS  1029.
    01 SQL-API-SQLGETDATALINKATTR           PIC S9(4) BINARY VALUE IS  1034.

    01 SQL-MAXIMUM-DATALINK-LENGTH          PIC S9(4) BINARY VALUE IS 20004.
