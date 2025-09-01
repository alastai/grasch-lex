
/*
The following C header file (.h) is a "digital artifact" that contains lines
of code in the C programming language to specify manifest constants and function prototypes
that may be used by application programs written in C that use SQL-implementations. 

A typical inclusion is:

    #include "sqlcli.h"

*/

    typedef unsigned char   SQLDATALINK;

    #define SQL_ATTR_DL_URL_COMPLETE                    3
    #define SQL_ATTR_DL_URL_PATH                        4
    #define SQL_ATTR_DL_URL_PATH_ONLY                   5
    #define SQL_ATTR_DL_URL_SCHEME                      6
    #define SQL_ATTR_DL_URL_SERVER                      7

    #define SQL_DATALINK                               70

    #define SQL_API_SQLBUILDDATALINK                 1029
    #define SQL_API_SQLGETDATALINKATTR               1034

    #define SQL_MAXIMUM_DATALINK_LENGTH             20004

    SQLRETURN  SQLBuildDataLink(SQLHSTMT StatementHandle,
               SQLCHAR *DataLocation, SQLINTEGER DataLocationLength,
               SQLCHAR *DataLink, SQLINTEGER DataLinkLength,
               SQLINTEGER *StringLength);
    SQLRETURN  SQLGetDataLinkAttr(SQLHSTMT StatementHandle,
               SQLSMALLINT Attribute,
               SQLCHAR *DataLink, SQLINTEGER DataLinkLength,
               SQLPOINTER Value, SQLINTEGER BufferLength,
               SQLINTEGER *StringLength);
