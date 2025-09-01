
/*
The following C header file (.h) is a "digital artifact" that contains lines
of code in the C programming language to specify manifest constants and function prototypes
that may be used by application programs written in C that use SQL-implementations. 

A typical inclusion is:

    #include "sqlcli.h"

*/

    /* sqlcli.h  Header File for SQL CLI.
     * The actual header file shall contain at least the information
     * specified here, except that the comments may vary.
                                                                 */
    /* API declaration data types                                */
    typedef unsigned char   SQLCHAR;
    typedef void *          SQLPOINTER;
    typedef unsigned char   SQLCLOB;
    typedef long            SQLCLOB_LOCATOR;
    typedef unsigned char   SQLBLOB;
    typedef long            SQLBLOB_LOCATOR;
    typedef unsigned char   SQLNUMERIC;
    typedef unsigned char   SQLDECIMAL;
    typedef short           SQLSMALLINT;
    typedef long            SQLINTEGER;
    typedef long long       SQLBIGINT;
    typedef float           SQLREAL;
    typedef double          SQLDOUBLE;
    typedef unsigned char   SQLDATE;
    typedef unsigned char   SQLTIME;
    typedef unsigned char   SQLTIMESTAMP;
    typedef unsigned char   SQLINTERVAL;
    typedef long            SQLUDT_LOCATOR;
    typedef unsigned char   SQLREF;
    typedef long            SQLARRAY_LOCATOR;
    typedef long            SQLMULTISET_LOCATOR;
    /* Function return type                                      */
    typedef SQLSMALLINT     SQLRETURN;
    /* Generic data structures                                   */
    typedef SQLINTEGER      SQLHENV;    /* environment handle    */
    typedef SQLINTEGER      SQLHDBC;    /* connection handle     */
    typedef SQLINTEGER      SQLHSTMT;   /* statement handle      */
    typedef SQLINTEGER      SQLHDESC;   /* descriptor handle     */
    /* Special length/indicator values                           */
    #define SQL_NULL_DATA                              -1
    #define SQL_DATA_AT_EXEC                           -2
    /* Return values from functions                              */
    #define SQL_SUCCESS                                 0
    #define SQL_SUCCESS_WITH_INFO                       1
    #define SQL_NEED_DATA                              99
    #define SQL_NO_DATA                               100
    #define SQL_ERROR                                  -1
    #define SQL_INVALID_HANDLE                         -2
    /* Row status values after a call to a fetch function        */
    #define SQL_ROW_SUCCESS                             0
    #define SQL_ROW_SUCCESS_WITH_INFO                   6
    #define SQL_ROW_ERROR                               5
    #define SQL_ROW_NO_ROW                              3
    /* Test for SQL_SUCCESS or SQL_SUCCESS_WITH_INFO             */
    #define SQL_SUCCEEDED(rc) (((rc)&(~1))==0)
    /* flags for null-terminated string                          */
    #define SQL_NTS                                    -3
    #define SQL_NTSL                                  -3L
    /* Maximum message length                                    */
    #define SQL_MAXIMUM_MESSAGE_LENGTH                512
    /* Handle type identifiers                                   */
    #define SQL_HANDLE_ENV                              1
    #define SQL_HANDLE_DBC                              2
    #define SQL_HANDLE_STMT                             3
    #define SQL_HANDLE_DESC                             4
    /* Environment attribute                                     */
    #define SQL_ATTR_OUTPUT_NTS                     10001
    /* Connection attribute */
    #define SQL_ATTR_AUTO_IPD                       10001
    #define SQL_ATTR_SAVEPOINT_NAME                 10027
    /* Statement attributes                                      */
    #define SQL_ATTR_CURSOR_SCROLLABLE                 -1
    #define SQL_ATTR_CURSOR_SENSITIVITY                -2
    #define SQL_ATTR_CURSOR_HOLDABLE                   -3
    #define SQL_ATTR_APP_ROW_DESC                   10010
    #define SQL_ATTR_APP_PARAM_DESC                 10011
    #define SQL_ATTR_IMP_ROW_DESC                   10012
    #define SQL_ATTR_IMP_PARAM_DESC                 10013
    #define SQL_ATTR_METADATA_ID                    10014
    #define SQL_ATTR_CURRENT_OF_POSITION            10027
    #define SQL_ATTR_NEST_DESCRIPTOR                10029
    /* Identifiers of fields in the SQL/CLI item descriptor area */
    #define SQL_DESC_ARRAY_SIZE                        20
    #define SQL_DESC_ARRAY_STATUS_POINTER              21
    #define SQL_DESC_DATETIME_INTERVAL_PRECISION       26
    #define SQL_DESC_ROWS_PROCESSED_POINTER            34
    #define SQL_DESC_COUNT                           1001
    #define SQL_DESC_TYPE                            1002
    #define SQL_DESC_LENGTH                          1003
    #define SQL_DESC_OCTET_LENGTH_POINTER            1004
    #define SQL_DESC_PRECISION                       1005
    #define SQL_DESC_SCALE                           1006
    #define SQL_DESC_DATETIME_INTERVAL_CODE          1007
    #define SQL_DESC_NULLABLE                        1008
    #define SQL_DESC_INDICATOR_POINTER               1009
    #define SQL_DESC_DATA_POINTER                    1010
    #define SQL_DESC_NAME                            1011
    #define SQL_DESC_UNNAMED                         1012
    #define SQL_DESC_OCTET_LENGTH                    1013
    #define SQL_DESC_COLLATION_CATALOG               1015
    #define SQL_DESC_COLLATION_SCHEMA                1016
    #define SQL_DESC_COLLATION_NAME                  1017
    #define SQL_DESC_CHARACTER_SET_CATALOG           1018
    #define SQL_DESC_CHARACTER_SET_SCHEMA            1019
    #define SQL_DESC_CHARACTER_SET_NAME              1020
    #define SQL_DESC_PARAMETER_MODE                  1021
    #define SQL_DESC_PARAMETER_ORDINAL_POSITION      1022
    #define SQL_DESC_PARAMETER_SPECIFIC_CATALOG      1023
    #define SQL_DESC_PARAMETER_SPECIFIC_SCHEMA       1024
    #define SQL_DESC_PARAMETER_SPECIFIC_NAME         1025
    #define SQL_DESC_UDT_CATALOG                     1026
    #define SQL_DESC_UDT_SCHEMA                      1027
    #define SQL_DESC_UDT_NAME                        1028
    #define SQL_DESC_KEY_TYPE                        1029
    #define SQL_DESC_KEY_MEMBER                      1030
    #define SQL_DESC_DYNAMIC_FUNCTION                1031
    #define SQL_DESC_DYNAMIC_FUNCTION_CODE           1032
    #define SQL_DESC_SCOPE_CATALOG                   1033
    #define SQL_DESC_SCOPE_SCHEMA                    1034
    #define SQL_DESC_SCOPE_NAME                      1035
    #define SQL_DESC_SPECIFIC_TYPE_CATALOG           1036
    #define SQL_DESC_SPECIFIC_TYPE_SCHEMA            1037
    #define SQL_DESC_SPECIFIC_TYPE_NAME              1038
    #define SQL_DESC_CURRENT_TRANSFORM_GROUP         1039
    #define SQL_DESC_CARDINALITY                     1040
    #define SQL_DESC_DEGREE                          1041
    #define SQL_DESC_LEVEL                           1042
    #define SQL_DESC_RETURNED_CARDINALITY_POINTER    1043
    #define SQL_DESC_TOP_LEVEL_COUNT                 1044
    #define SQL_DESC_USER_DEFINED_TYPE_CODE          1045
    #define SQL_DESC_ALLOC_TYPE                      1099
    /* Identifiers of fields in the diagnostics area             */
    #define SQL_DIAG_ROW_NUMBER                     -1248
    #define SQL_DIAG_COLUMN_NUMBER                  -1247
    #define SQL_DIAG_RETURNCODE                         1
    #define SQL_DIAG_NUMBER                             2
    #define SQL_DIAG_ROW_COUNT                          3
    #define SQL_DIAG_SQLSTATE                           4
    #define SQL_DIAG_NATIVE_CODE                        5
    #define SQL_DIAG_MESSAGE_TEXT                       6
    #define SQL_DIAG_DYNAMIC_FUNCTION                   7
    #define SQL_DIAG_CLASS_ORIGIN                       8
    #define SQL_DIAG_SUBCLASS_ORIGIN                    9
    #define SQL_DIAG_CONNECTION_NAME                   10
    #define SQL_DIAG_SERVER_NAME                       11
    #define SQL_DIAG_DYNAMIC_FUNCTION_CODE             12
    #define SQL_DIAG_MORE                              13
    #define SQL_DIAG_CONDITION_NUMBER                  14
    #define SQL_DIAG_CONSTRAINT_CATALOG                15
    #define SQL_DIAG_CONSTRAINT_SCHEMA                 16
    #define SQL_DIAG_CONSTRAINT_NAME                   17
    #define SQL_DIAG_CATALOG_NAME                      18
    #define SQL_DIAG_SCHEMA_NAME                       19
    #define SQL_DIAG_TABLE_NAME                        20
    #define SQL_DIAG_COLUMN_NAME                       21
    #define SQL_DIAG_CURSOR_NAME                       22
    #define SQL_DIAG_MESSAGE_LENGTH                    23
    #define SQL_DIAG_MESSAGE_OCTET_LENGTH              24
    #define SQL_DIAG_CONDITION_IDENTIFIER              25
    #define SQL_DIAG_PARAMETER_NAME                    26
    #define SQL_DIAG_ROUTINE_CATALOG                   27
    #define SQL_DIAG_ROUTINE_SCHEMA                    28
    #define SQL_DIAG_ROUTINE_NAME                      29
    #define SQL_DIAG_SPECIFIC_NAME                     30
    #define SQL_DIAG_TRIGGER_CATALOG                   31
    #define SQL_DIAG_TRIGGER_SCHEMA                    32
    #define SQL_DIAG_TRIGGER_NAME                      33
    #define SQL_DIAG_TRANSACTIONS_COMMITTED            34
    #define SQL_DIAG_TRANSACTIONS_ROLLED_BACK          35
    #define SQL_DIAG_TRANSACTION_ACTIVE                36
    #define SQL_DIAG_PARAMETER_MODE                    37
    #define SQL_DIAG_PARAMETER_ORDINAL_POSITION        38
    /* Dynamic function codes returned in diagnostics area       */
    #define SQL_DIAG_ALTER_DOMAIN                       3
    #define SQL_DIAG_ALTER_TABLE                        4
    #define SQL_DIAG_CALL                               7
    #define SQL_DIAG_CREATE_ASSERTION                   6
    #define SQL_DIAG_CREATE_CHARACTER_SET               8
    #define SQL_DIAG_CREATE_COLLATION                  10
    #define SQL_DIAG_CREATE_DOMAIN                     23
    #define SQL_DIAG_CREATE_SCHEMA                     64
    #define SQL_DIAG_CREATE_TABLE                      77
    #define SQL_DIAG_CREATE_TRANSLATION                79
    #define SQL_DIAG_CREATE_VIEW                       84
    #define SQL_DIAG_DELETE_WHERE                      19
    #define SQL_DIAG_DROP_ASSERTION                    24
    #define SQL_DIAG_DROP_CHARACTER_SET                25
    #define SQL_DIAG_DROP_COLLATION                    26
    #define SQL_DIAG_DROP_DOMAIN                       27
    #define SQL_DIAG_DROP_SCHEMA                       31
    #define SQL_DIAG_DROP_TABLE                        32
    #define SQL_DIAG_DROP_TRANSLATION                  33
    #define SQL_DIAG_DROP_VIEW                         36
    #define SQL_DIAG_DYNAMIC_DELETE_CURSOR             54
    #define SQL_DIAG_DYNAMIC_UPDATE_CURSOR             55
    #define SQL_DIAG_GRANT                             48
    #define SQL_DIAG_INSERT                            50
    #define SQL_DIAG_MERGE                            128
    #define SQL_DIAG_REVOKE                            59
    #define SQL_DIAG_SELECT                            41
    #define SQL_DIAG_SELECT_CURSOR                     85
    #define SQL_DIAG_SET_CATALOG                       66
    #define SQL_DIAG_SET_CONSTRAINT                    68
    #define SQL_DIAG_SET_NAMES                         72
    #define SQL_DIAG_SET_SCHEMA                        74
    #define SQL_DIAG_SET_SESSION_AUTHORIZATION         76
    #define SQL_DIAG_SET_TIME_ZONE                     71
    #define SQL_DIAG_SET_TRANSACTION                   75
    #define SQL_DIAG_UNKNOWN_STATEMENT                  0
    #define SQL_DIAG_UPDATE_WHERE                      82
    /* SQL data type codes                                       */
    #define SQL_CHAR                                    1
    #define SQL_NUMERIC                                 2
    #define SQL_DECIMAL                                 3
    #define SQL_INTEGER                                 4
    #define SQL_SMALLINT                                5
    #define SQL_FLOAT                                   6
    #define SQL_REAL                                    7
    #define SQL_DOUBLE                                  8
    #define SQL_DATETIME                                9
    #define SQL_INTERVAL                               10
    #define SQL_VARCHAR                                12
    #define SQL_BOOLEAN                                16
    #define SQL_UDT                                    17
    #define SQL_UDT_LOCATOR                            18
    #define SQL_ROW                                    19
    #define SQL_REF                                    20
    #define SQL_BIGINT                                 25
    #define SQL_BLOB                                   30
    #define SQL_BLOB_LOCATOR                           31
    #define SQL_CLOB                                   40
    #define SQL_CLOB_LOCATOR                           41
    #define SQL_ARRAY                                  50
    #define SQL_ARRAY_LOCATOR                          51
    #define SQL_MULTISET                               55
    #define SQL_MULTISET_LOCATOR                       56
    /*      Concise codes for datetime and interval data types   */
    #define SQL_TYPE_DATE                              91
    #define SQL_TYPE_TIME                              92
    #define SQL_TYPE_TIME_WITH_TIMEZONE                94
    #define SQL_TYPE_TIMESTAMP                         93
    #define SQL_TYPE_TIMESTAMP_WITH_TIMEZONE           95
    #define SQL_INTERVAL_DAY                          103
    #define SQL_INTERVAL_DAY_TO_HOUR                  108
    #define SQL_INTERVAL_DAY_TO_MINUTE                109
    #define SQL_INTERVAL_DAY_TO_SECOND                110
    #define SQL_INTERVAL_HOUR                         104
    #define SQL_INTERVAL_HOUR_TO_MINUTE               111
    #define SQL_INTERVAL_HOUR_TO_SECOND               112
    #define SQL_INTERVAL_MINUTE                       105
    #define SQL_INTERVAL_MINUTE_TO_SECOND             113
    #define SQL_INTERVAL_MONTH                        102
    #define SQL_INTERVAL_SECOND                       106
    #define SQL_INTERVAL_YEAR                         101
    #define SQL_INTERVAL_YEAR_TO_MONTH                107
    /* User-defined data type codes                              */
    #define SQL_DISTINCT                                1
    #define SQL_STRUCTURED                              2
    /*      GetTypeInfo() request for all data types             */
    #define SQL_ALL_TYPES                               0
    /* BindCol() and BindParameter() default conversion code     */
    #define SQL_DEFAULT                                99
    /*  GetData() and \() code indicating that the
        application parameter descriptor specifies the data type */
    #define SQL_APD_TYPE                              -99
    #define SQL_ARD_TYPE                              -99
    /* Date/time type subcodes                                   */
    #define SQL_CODE_DATE                               1
    #define SQL_CODE_TIME                               2
    #define SQL_CODE_TIMESTAMP                          3
    #define SQL_CODE_TIME_ZONE                          4
    #define SQL_CODE_TIMESTAMP_ZONE                     5
    /* Interval qualifier codes                                  */
    #define SQL_DAY                                     3
    #define SQL_DAY_TO_HOUR                             8
    #define SQL_DAY_TO_MINUTE                           9
    #define SQL_DAY_TO_SECOND                          10
    #define SQL_HOUR                                    4
    #define SQL_HOUR_TO_MINUTE                         11
    #define SQL_HOUR_TO_SECOND                         12
    #define SQL_MINUTE                                  5
    #define SQL_MINUTE_TO_SECOND                       13
    #define SQL_MONTH                                   2
    #define SQL_SECOND                                  6
    #define SQL_YEAR                                    1
    #define SQL_YEAR_TO_MONTH                           7
    /* CLI option values                                         */
    #define SQL_FALSE                                   0
    #define SQL_TRUE                                    1
    #define SQL_NONSCROLLABLE                           0
    #define SQL_SCROLLABLE                              1
    #define SQL_NONHOLDABLE                             0
    #define SQL_HOLDABLE                                1
    #define SQL_INITIALLY_DEFERRED                      5
    #define SQL_INITIALLY_IMMEDIATE                     6
    #define SQL_NOT_DEFERRABLE                          7
    /* Parameter mode values                                     */
    #define SQL_PARAM_MODE_IN                           1
    #define SQL_PARAM_MODE_OUT                          4
    #define SQL_PARAM_MODE_INOUT                        2
    /* Codes used for FetchOrientation                           */
    #define SQL_FETCH_NEXT                              1
    #define SQL_FETCH_FIRST                             2
    #define SQL_FETCH_LAST                              3
    #define SQL_FETCH_PRIOR                             4
    #define SQL_FETCH_ABSOLUTE                          5
    #define SQL_FETCH_RELATIVE                          6
    /* Values of NULLABLE field in descriptor                    */
    #define SQL_NO_NULLS                                0
    #define SQL_NULLABLE                                1
    /* Values returned by GetTypeInfo for the SEARCHABLE column  */
    #define SQL_PRED_NONE                               0
    #define SQL_PRED_CHAR                               1
    #define SQL_PRED_BASIC                              2
    /* Values of UNNAMED field in descriptor                     */
    #define SQL_NAMED                                   0
    #define SQL_UNNAMED                                 1
    /* Values of ALLOC_TYPE field in descriptor                  */
    #define SQL_DESC_ALLOC_AUTO                         1
    #define SQL_DESC_ALLOC_USER                         2
    /* EndTran() options */
    #define SQL_COMMIT                                  0
    #define SQL_ROLLBACK                                1
    #define SQL_SAVEPOINT_NAME_ROLLBACK                 2
    #define SQL_SAVEPOINT_NAME_RELEASE                  4
    #define SQL_COMMIT_AND_CHAIN                        6
    #define SQL_ROLLBACK_AND_CHAIN                      7
    /* FreeStmt() options                                        */
    #define SQL_CLOSE_CURSOR                            0
    #define SQL_FREE_HANDLE                             1
    #define SQL_UNBIND_COLUMNS                          2
    #define SQL_UNBIND_PARAMETERS                       3
    #define SQL_REALLOCATE                              4
    /* Provided for backwards compatibility                      */
    #define SQL_CLOSE                                   0
    #define SQL_DROP                                    1
    #define SQL_UNBIND                                  2
    #define SQL_RESET_PARAMS                            3
    /* Null handle used when allocating HENV                     */
    #define SQL_NULL_HANDLE                            0L
    /* Null handles returned by AllocHandle()                    */
    #define SQL_NULL_HENV                 SQL_NULL_HANDLE
    #define SQL_NULL_HDBC                 SQL_NULL_HANDLE
    #define SQL_NULL_HSTMT                SQL_NULL_HANDLE
    #define SQL_NULL_HDESC                SQL_NULL_HANDLE
    /*      GetFunctions values to identify CLI routines         */
    #define SQL_API_SQLALLOCCONNECT                     1
    #define SQL_API_SQLALLOCENV                         2
    #define SQL_API_SQLALLOCHANDLE                   1001
    #define SQL_API_SQLALLOCSTMT                        3
    #define SQL_API_SQLBINDCOL                          4
    #define SQL_API_SQLBINDPARAMETER                   72
    #define SQL_API_SQLCANCEL                           5
    #define SQL_API_SQLCLOSECURSOR                   1003
    #define SQL_API_SQLCOLATTRIBUTE                     6
    #define SQL_API_SQLCOLUMNPRIVILEGES                56
    #define SQL_API_SQLCOLUMNS                         40
    #define SQL_API_SQLCONNECT                          7
    #define SQL_API_SQLCOPYDESC                      1004
    #define SQL_API_SQLDATASOURCES                     57
    #define SQL_API_SQLDESCRIBECOL                      8
    #define SQL_API_SQLDISCONNECT                       9
    #define SQL_API_SQLENDTRAN                       1005
    #define SQL_API_SQLERROR                           10
    #define SQL_API_SQLEXECDIRECT                      11
    #define SQL_API_SQLEXECUTE                         12
    #define SQL_API_SQLFETCH                           13
    #define SQL_API_SQLFETCHSCROLL                   1021
    #define SQL_API_SQLFOREIGNKEYS                     60
    #define SQL_API_SQLFREECONNECT                     14
    #define SQL_API_SQLFREEENV                         15
    #define SQL_API_SQLFREEHANDLE                    1006
    #define SQL_API_SQLFREESTMT                        16
    #define SQL_API_SQLGETCONNECTATTR                1007
    #define SQL_API_SQLGETCURSORNAME                   17
    #define SQL_API_SQLGETDATA                         43
    #define SQL_API_SQLGETDESCFIELD                  1008
    #define SQL_API_SQLGETDESCREC                    1009
    #define SQL_API_SQLGETDIAGFIELD                  1010
    #define SQL_API_SQLGETDIAGREC                    1011
    #define SQL_API_SQLGETENVATTR                    1012
    #define SQL_API_SQLGETFEATUREINFO                1027
    #define SQL_API_SQLGETFUNCTIONS                    44
    #define SQL_API_SQLGETINFO                         45
    #define SQL_API_SQLGETLENGTH                     1022
    #define SQL_API_SQLGETPARAMDATA                  1025
    #define SQL_API_SQLGETPOSITION                   1023
    #define SQL_API_SQLGETSESSIONINFO                1028
    #define SQL_API_SQLGETSTMTATTR                   1014
    #define SQL_API_SQLGETSUBSTRING                  1024
    #define SQL_API_SQLGETTYPEINFO                     47
    #define SQL_API_SQLMORERESULTS                     61
    #define SQL_API_SQLNEXTRESULT                      73
    #define SQL_API_SQLNUMRESULTCOLS                   18
    #define SQL_API_SQLPARAMDATA                       48
    #define SQL_API_SQLPREPARE                         19
    #define SQL_API_SQLPRIMARYKEYS                     65
    #define SQL_API_SQLPUTDATA                         49
    #define SQL_API_SQLROWCOUNT                        20
    #define SQL_API_SQLSETCONNECTATTR                1016
    #define SQL_API_SQLSETCURSORNAME                   21
    #define SQL_API_SQLSETDESCFIELD                  1017
    #define SQL_API_SQLSETDESCREC                    1018
    #define SQL_API_SQLSETENVATTR                    1019
    #define SQL_API_SQLSETSTMTATTR                   1020
    #define SQL_API_SQLSPECIALCOLUMNS                  52
    #define SQL_API_SQLSTARTTRAN                       74
    #define SQL_API_SQLTABLES                          54
    #define SQL_API_SQLTABLEPRIVILEGES                 70
    /*      Information requested by GetInfo()                   */
    #define SQL_MAXIMUM_DRIVER_CONNECTIONS              0
    #define SQL_MAXIMUM_CONCURRENT_ACTIVITIES           1
    #define SQL_DATA_SOURCE_NAME                        2
WG3:XRH-017 One line deleted

    #define SQL_SERVER_NAME                            13
    #define SQL_SEARCH_PATTERN_ESCAPE                  14
    #define SQL_DBMS_NAME                              17
    #define SQL_DBMS_VERSION                           18
    #define SQL_CURSOR_COMMIT_BEHAVIOR                 23
WG3:XRH-017 One line deleted

    #define SQL_DEFAULT_TRANSACTION_ISOLATION          26
    #define SQL_IDENTIFIER_CASE                        28
    #define SQL_MAXIMUM_COLUMN_NAME_LENGTH             30
    #define SQL_MAXIMUM_CURSOR_NAME_LENGTH             31
    #define SQL_MAXIMUM_SCHEMA_NAME_LENGTH             32
    #define SQL_MAXIMUM_CATALOG_NAME_LENGTH            34
    #define SQL_MAXIMUM_TABLE_NAME_LENGTH              35
WG3:XRH-017 One line deleted

    #define SQL_TRANSACTION_CAPABLE                    46
WG3:XRH-017 Four lines deleted

    #define SQL_NULL_COLLATION                         85
WG3:XRH-017 Two lines deleted

    #define SQL_SPECIAL_CHARACTERS                     94
    #define SQL_MAXIMUM_COLUMNS_IN_GROUP_BY            97
    #define SQL_MAXIMUM_COLUMNS_IN_ORDER_BY            99
    #define SQL_MAXIMUM_COLUMNS_IN_SELECT             100
    #define SQL_MAXIMUM_COLUMNS_IN_TABLE              101
    #define SQL_MAXIMUM_TABLES_IN_SELECT              106
    #define SQL_MAXIMUM_USER_NAME_LENGTH              107
WG3:XRH-017 Three lines deleted

    #define SQL_CATALOG_NAME                        10003
    #define SQL_COLLATING_SEQUENCE                  10004
    #define SQL_MAXIMUM_IDENTIFIER_LENGTH           10005
    #define SQL_MAXIMUM_STMT_OCTETS                 20000
    #define SQL_MAXIMUM_STMT_OCTETS_DATA            20001
    #define SQL_MAXIMUM_STMT_OCTETS_SCHEMA          20002
    /*      Information requested by GetSessionInfo()            */
    #define SQL_CURRENT_USER                           47
    #define SQL_CURRENT_DEFAULT_TRANSFORM_GROUP     20004
    #define SQL_CURRENT_PATH                        20005
    #define SQL_CURRENT_ROLE                        20006
    #define SQL_SESSION_USER                        20007
    #define SQL_SYSTEM_USER                         20008
    #define SQL_CURRENT_CATALOG                     20009
    #define SQL_CURRENT_SCHEMA                      20010
    /* Statement attribute values for cursor sensitivity         */
    #define SQL_ASENSITIVE                    0x00000000L
    #define SQL_INSENSITIVE                   0x00000001L
    #define SQL_SENSITIVE                     0x00000002L
    /* Define SQL_UNSPECIFIED for backwards compatibility        */
    #define SQL_UNSPECIFIED                SQL_ASENSITIVE
    /* SQL_ALTER_TABLE bitmasks                                  */
    #define SQL_AT_ADD_COLUMN                 0x00000001L
    #define SQL_AT_DROP_COLUMN                0x00000002L
    #define SQL_AT_ALTER_COLUMN               0x00000004L
    #define SQL_AT_ADD_CONSTRAINT             0x00000008L
    #define SQL_AT_DROP_CONSTRAINT            0x00000010L
    /* SQL_CURSOR_COMMIT_BEHAVIOR values                         */
    #define SQL_CB_DELETE                               0
    #define SQL_CB_CLOSE                                1
    #define SQL_CB_PRESERVE                             2
    /* SQL_FETCH_DIRECTION bitmasks                              */
    #define SQL_FD_FETCH_NEXT                 0x00000001L
    #define SQL_FD_FETCH_FIRST                0x00000002L
    #define SQL_FD_FETCH_LAST                 0x00000004L
    #define SQL_FD_FETCH_PRIOR                0x00000008L
    #define SQL_FD_FETCH_ABSOLUTE             0x00000010L
    #define SQL_FD_FETCH_RELATIVE             0x00000020L
    /* SQL_GETDATA_EXTENSIONS bitmasks                           */
    #define SQL_GD_ANY_COLUMN                 0x00000001L
    #define SQL_GD_ANY_ORDER                  0x00000002L
    /* SQL_IDENTIFIER_CASE values                                */
    #define SQL_IC_UPPER                                1
    #define SQL_IC_LOWER                                2
    #define SQL_IC_SENSITIVE                            3
    #define SQL_IC_MIXED                                4
    /* SQL_NULL_COLLATION values                                 */
    #define SQL_NC_HIGH                                 1
    #define SQL_NC_LOW                                  2
    /* SQL_OUTER_JOIN_CAPABILITIES bitmasks                      */
    #define SQL_OUTER_JOIN_LEFT               0x00000001L
    #define SQL_OUTER_JOIN_RIGHT              0x00000002L
    #define SQL_OUTER_JOIN_FULL               0x00000004L
    #define SQL_OUTER_JOIN_NESTED             0x00000008L
    #define SQL_OUTER_JOIN_NOT_ORDERED        0x00000010L
    #define SQL_OUTER_JOIN_INNER              0x00000020L
    #define SQL_OUTER_JOIN_ALL_COMPARISON_OPS 0x00000040L
    /* SQL_SCROLL_CONCURRENCY bitmasks                           */
    #define SQL_SCCO_READ_ONLY                0x00000001L
    #define SQL_SCCO_LOCK                     0x00000002L
    #define SQL_SCCO_OPT_ROWVER               0x00000004L
    #define SQL_SCCO_OPT_VALUES               0x00000008L
    /* SQL_TRANSACTION_CAPABLE values                            */
    #define SQL_TC_NONE                                 0
    #define SQL_TC_DML                                  1
    #define SQL_TC_ALL                                  2
    #define SQL_TC_DDL_COMMIT                           3
    #define SQL_TC_DDL_IGNORE                           4
    /* SQL_TRANSACTION_ISOLATION bitmasks                        */
    #define SQL_TRANSACTION_READ_UNCOMMITTED  0x00000001L
    #define SQL_TRANSACTION_READ_COMMITTED    0x00000002L
    #define SQL_TRANSACTION_REPEATABLE_READ   0x00000004L
    #define SQL_TRANSACTION_SERIALIZABLE      0x00000008L
    /* SQL_TRANSACTION_ACCESS_MODE bitmasks                      */
    #define SQL_TRANSACTION_READ_ONLY         0x00000001L
    #define SQL_TRANSACTION_READ_WRITE        0x00000002L
/* Column types and scopes in SpecialColumns */
    #define SQL_BEST_ROWID                             1
    #define SQL_SCOPE_CURROW                           0
    #define SQL_SCOPE_TRANSACTION                      1
    #define SQL_SCOPE_SESSION                          2
    #define SQL_PC_UNKNOWN                             0
    #define SQL_PC_NOT_PSEUDO                          1
    #define SQL_PC_PSEUDO                              2
/* Foreign Key UPDATE and DELETE rules */
    #define SQL_CASCADE                                0
    #define SQL_RESTRICT                               1
    #define SQL_SET_NULL                               2
    #define SQL_NO_ACTION                              3
    #define SQL_SET_DEFAULT                            4
    /* Special parameter values                                  */
    #define SQL_ALL_CATALOGS                          "%"
    #define SQL_ALL_SCHEMAS                           "%"
    #define SQL_ALL_TABLE_TYPES                       "%"
    /* Function prototypes                                       */
    SQLRETURN  SQLAllocConnect(SQLHENV EnvironmentHandle,
               SQLHDBC *ConnectionHandle);
    SQLRETURN  SQLAllocEnv(SQLHENV *EnvironmentHandle);
    SQLRETURN  SQLAllocHandle(SQLSMALLINT HandleType,
               SQLINTEGER InputHandle, SQLINTEGER *OutputHandle);
    SQLRETURN  SQLAllocStmt(SQLHDBC ConnectionHandle,
               SQLHSTMT *StatementHandle);
    SQLRETURN  SQLBindCol(SQLHSTMT StatementHandle,
               SQLSMALLINT ColumnNumber, SQLSMALLINT BufferType,
               SQLPOINTER Data, SQLINTEGER BufferLength,
               SQLINTEGER *StrLen_or_Ind);
    SQLRETURN  SQLBindParameter(SQLHSTMT StatementHandle,
               SQLSMALLINT ParamNumber, SQLSMALLINT InputOutputMode,
               SQLSMALLINT ValueType, SQLSMALLINT ParameterType,
               SQLINTEGER ColumnSize, SQLSMALLINT DecimalDigits,
               SQLPOINTER ParameterValue, SQLINTEGER BufferLength,
               SQLINTEGER *StrLen_or_Ind);
    SQLRETURN  SQLCancel(SQLHSTMT StatementHandle);
    SQLRETURN  SQLCloseCursor(SQLHSTMT StatementHandle);
    SQLRETURN  SQLColAttribute(SQLHSTMT StatementHandle,
               SQLSMALLINT ColumnNumber, SQLSMALLINT FieldIdentifier,
               SQLCHAR *CharacterAttribute, SQLSMALLINT BufferLength,
               SQLSMALLINT *StringLength, SQLINTEGER *NumericAttribute);
    SQLRETURN  SQLColumnPrivileges(SQLHSTMT StatementHandle,
               SQLCHAR *CatalogName, SQLSMALLINT NameLength1,
               SQLCHAR *SchemaName, SQLSMALLINT NameLength2,
               SQLCHAR *TableName, SQLSMALLINT NameLength3,
               SQLCHAR *ColumnName, SQLSMALLINT NameLength4 );
    SQLRETURN  SQLColumns(SQLHSTMT StatementHandle,
               SQLCHAR *CatalogName, SQLSMALLINT NameLength1,
               SQLCHAR *SchemaName, SQLSMALLINT NameLength2,
               SQLCHAR *TableName, SQLSMALLINT NameLength3,
               SQLCHAR *ColumnName, SQLSMALLINT NameLength4 );
    SQLRETURN  SQLConnect(SQLHDBC ConnectionHandle,
               SQLCHAR *ServerName, SQLSMALLINT NameLength1,
               SQLCHAR *UserName, SQLSMALLINT NameLength2,
               SQLCHAR *Authentication, SQLSMALLINT NameLength3);
    SQLRETURN  SQLCopyDesc(SQLHDESC SourceDescHandle,
               SQLHDESC TargetDescHandle);
    SQLRETURN  SQLDataSources(SQLHENV EnvironmentHandle,
               SQLSMALLINT Direction, SQLCHAR *ServerName,
               SQLSMALLINT BufferLength1, SQLSMALLINT *NameLength1,
               SQLCHAR *Description, SQLSMALLINT BufferLength2,
               SQLSMALLINT *NameLength2);
    SQLRETURN  SQLDescribeCol(SQLHSTMT StatementHandle,
               SQLSMALLINT ColumnNumber, SQLCHAR *ColumnName,
               SQLSMALLINT BufferLength, SQLSMALLINT *NameLength,
               SQLSMALLINT *DataType, SQLINTEGER *ColumnSize,
               SQLSMALLINT *DecimalDigits, SQLSMALLINT *Nullable);
    SQLRETURN  SQLDisconnect(SQLHDBC ConnectionHandle);
    SQLRETURN  SQLEndTran(SQLSMALLINT HandleType, SQLINTEGER Handle,
               SQLSMALLINT CompletionType);
    SQLRETURN  SQLError(SQLHENV EnvironmentHandle,
               SQLHDBC ConnectionHandle, SQLHSTMT StatementHandle,
               SQLCHAR *Sqlstate, SQLINTEGER *NativeError,
               SQLCHAR *MessageText, SQLSMALLINT BufferLength,
               SQLSMALLINT *TextLength);
    SQLRETURN  SQLExecDirect(SQLHSTMT StatementHandle,
               SQLCHAR *StatementText, SQLINTEGER TextLength);
    SQLRETURN  SQLExecute(SQLHSTMT StatementHandle);
    SQLRETURN  SQLFetch(SQLHSTMT StatementHandle);
    SQLRETURN  SQLFetchScroll(SQLHSTMT StatementHandle,
               SQLSMALLINT FetchOrientation, SQLINTEGER FetchOffset);
    SQLRETURN  SQLForeignKeys(SQLHSTMT StatementHandle,
               SQLCHAR *PKCatalogName, SQLSMALLINT NameLength1,
               SQLCHAR *PKSchemaName, SQLSMALLINT NameLength2,
               SQLCHAR *PKTableName, SQLSMALLINT NameLength3,
               SQLCHAR *FKCatalogName, SQLSMALLINT NameLength4,
               SQLCHAR *FKSchemaName, SQLSMALLINT NameLength5,
               SQLCHAR *FKTableName, SQLSMALLINT NameLength6);
    SQLRETURN  SQLFreeConnect(SQLHDBC ConnectionHandle);
    SQLRETURN  SQLFreeEnv(SQLHENV EnvironmentHandle);
    SQLRETURN  SQLFreeHandle(SQLSMALLINT HandleType,
               SQLINTEGER Handle);
    SQLRETURN  SQLFreeStmt(SQLHSTMT StatementHandle, SQLSMALLINT Option);
    SQLRETURN  SQLGetConnectAttr(SQLHDBC ConnectionHandle,
               SQLINTEGER Attribute, SQLPOINTER Value,
               SQLINTEGER BufferLength, SQLINTEGER *StringLength);
    SQLRETURN  SQLGetCursorName(SQLHSTMT StatementHandle,
               SQLCHAR *CursorName, SQLSMALLINT BufferLength,
               SQLSMALLINT *NameLength);
    SQLRETURN  SQLGetData(SQLHSTMT StatementHandle,
               SQLSMALLINT ColumnNumber, SQLSMALLINT TargetType,
               SQLPOINTER TargetValue, SQLINTEGER BufferLength,
               SQLINTEGER *StrLen_or_Ind);
    SQLRETURN  SQLGetDescField(SQLHDESC DescriptorHandle,
               SQLSMALLINT RecordNumber, SQLSMALLINT FieldIdentifier,
               SQLPOINTER Value, SQLINTEGER BufferLength,
               SQLINTEGER *StringLength);
    SQLRETURN  SQLGetDescRec(SQLHDESC DescriptorHandle,
               SQLSMALLINT RecordNumber, SQLCHAR *Name,
               SQLSMALLINT BufferLength, SQLSMALLINT *NameLength,
               SQLSMALLINT *Type, SQLSMALLINT *SubType,
               SQLINTEGER *Length, SQLSMALLINT *Precision,
               SQLSMALLINT *Scale, SQLSMALLINT *Nullable);
    SQLRETURN  SQLGetDiagField(SQLSMALLINT HandleType,
               SQLINTEGER Handle, SQLSMALLINT RecordNumber,
               SQLSMALLINT DiagIdentifier, SQLPOINTER DiagInfo,
               SQLSMALLINT BufferLength, SQLSMALLINT *StringLength);
    SQLRETURN  SQLGetDiagRec(SQLSMALLINT HandleType, SQLINTEGER Handle,
               SQLSMALLINT RecordNumber, SQLCHAR *Sqlstate,
               SQLINTEGER *NativeError, SQLCHAR *MessageText,
               SQLSMALLINT BufferLength, SQLSMALLINT *TextLength);
    SQLRETURN  SQLGetEnvAttr(SQLHENV EnvironmentHandle,
               SQLINTEGER Attribute, SQLPOINTER Value,
               SQLINTEGER BufferLength, SQLINTEGER *StringLength);
    SQLRETURN  SQLGetFeatureInfo(SQLHDBC ConnectionHandle,
               SQLCHAR *FeatureType, SQLSMALLINT FeatureTypeLength,
               SQLCHAR *FeatureId, SQLSMALLINT FeatureIdLength,
               SQLCHAR *SubFeatureId, SQLSMALLINT SubFeatureIdLength,
               SQLSMALLINT *Supported);
    SQLRETURN  SQLGetFunctions(SQLHDBC ConnectionHandle,
               SQLSMALLINT FunctionId, SQLSMALLINT *Supported);
    SQLRETURN  SQLGetInfo(SQLHDBC ConnectionHandle,
               SQLSMALLINT InfoType, SQLPOINTER InfoValue,
               SQLSMALLINT BufferLength, SQLSMALLINT *StringLength);
    SQLRETURN  SQLGetLength(SQLHSTMT StatementHandle,
               SQLSMALLINT LocatorType, SQLINTEGER Locator,
               SQLINTEGER *StringLength, SQLINTEGER *IndicatorValue);
    SQLRETURN  SQLGetParamData(SQLHSTMT StatementHandle,
               SQLSMALLINT ParameterNumber, SQLSMALLINT TargetType,
               SQLPOINTER TargetValue, SQLINTEGER BufferLength,
               SQLINTEGER *StrLen_or_Ind);
    SQLRETURN  SQLGetPosition(SQLHSTMT StatementHandle,
               SQLSMALLINT LocatorType, SQLINTEGER SourceLocator,
               SQLINTEGER SearchLocator, SQLCHAR *SearchLiteral,
               SQLINTEGER SearchLiteralLength, SQLINTEGER FromPosition,
               SQLINTEGER *LocatedAt, SQLINTEGER *IndicatorValue);
    SQLRETURN  SQLGetSessionInfo(SQLHDBC ConnectionHandle,
               SQLSMALLINT InfoType, SQLPOINTER InfoValue,
               SQLSMALLINT BufferLength, SQLSMALLINT *StringLength);
    SQLRETURN  SQLGetStmtAttr(SQLHSTMT StatementHandle,
               SQLINTEGER Attribute, SQLPOINTER Value,
               SQLINTEGER BufferLength, SQLINTEGER *StringLength);
    SQLRETURN  SQLGetSubString(SQLHSTMT StatementHandle,
               SQLSMALLINT LocatorType, SQLINTEGER SourceLocator,
               SQLINTEGER FromPosition, SQLINTEGER ForLength,
               SQLSMALLINT TargetType, SQLPOINTER TargetValue,
               SQLINTEGER BufferLength, SQLINTEGER *StringLength,
               SQLINTEGER *IndicatorValue);
    SQLRETURN  SQLGetTypeInfo(SQLHSTMT StatementHandle,
               SQLSMALLINT DataType);
    SQLRETURN  SQLMoreResults(SQLHSTMT StatementHandle);
    SQLRETURN  SQLNextResult(SQLHSTMT StatementHandle1,
               SQLHSTMT *StatementHandle2);
    SQLRETURN  SQLNumResultCols(SQLHSTMT StatementHandle,
               SQLSMALLINT *ColumnCount);
    SQLRETURN  SQLParamData(SQLHSTMT StatementHandle,
               SQLPOINTER *Value);
    SQLRETURN  SQLPrepare(SQLHSTMT StatementHandle,
               SQLCHAR *StatementText, SQLINTEGER TextLength);
    SQLRETURN  SQLPrimaryKeys(SQLHSTMT StatementHandle,
               SQLCHAR *CatalogName, SQLSMALLINT NameLength1,
               SQLCHAR *SchemaName, SQLSMALLINT NameLength2,
               SQLCHAR *TableName, SQLSMALLINT NameLength3);
    SQLRETURN  SQLPutData(SQLHSTMT StatementHandle,
               SQLPOINTER Data, SQLINTEGER StrLen_or_Ind);
    SQLRETURN  SQLRowCount(SQLHSTMT StatementHandle,
               SQLINTEGER *RowCount);
    SQLRETURN  SQLSetConnectAttr(SQLHDBC ConnectionHandle,
               SQLINTEGER Attribute, SQLPOINTER Value,
               SQLINTEGER StringLength);
    SQLRETURN  SQLSetCursorName(SQLHSTMT StatementHandle,
               SQLCHAR *CursorName, SQLSMALLINT NameLength);
    SQLRETURN  SQLSetDescField(SQLHDESC DescriptorHandle,
               SQLSMALLINT RecordNumber, SQLSMALLINT FieldIdentifier,
               SQLPOINTER Value, SQLINTEGER BufferLength);
    SQLRETURN  SQLSetDescRec(SQLHDESC DescriptorHandle,
               SQLSMALLINT RecordNumber, SQLSMALLINT Type,
               SQLSMALLINT SubType, SQLINTEGER Length,
               SQLSMALLINT Precision, SQLSMALLINT Scale,
               SQLPOINTER Data, SQLINTEGER *StringLength,
               SQLINTEGER *Indicator);
    SQLRETURN  SQLSetEnvAttr(SQLHENV EnvironmentHandle,
               SQLINTEGER Attribute, SQLPOINTER Value,
               SQLINTEGER StringLength);
    SQLRETURN  SQLSetStmtAttr(SQLHSTMT StatementHandle,
               SQLINTEGER Attribute, SQLPOINTER Value,
               SQLINTEGER StringLength);
    SQLRETURN  SQLSpecialColumns(SQLHSTMT StatementHandle,
               SQLSMALLINT IdentifierType, SQLCHAR *CatalogName,
               SQLSMALLINT NameLength1, SQLCHAR *SchemaName,
               SQLSMALLINT NameLength2, SQLCHAR *TableName,
               SQLSMALLINT NameLength3, SQLSMALLINT Scope,
               SQLSMALLINT Nullable);
    SQLRETURN  SQLStartTran(SQLSMALLINT HandleType,
               SQLINTEGER Handle, SQLINTEGER AccessMode,
               SQLINTEGER IsolationLevel);
    SQLRETURN  SQLTablePrivileges(SQLHSTMT StatementHandle,
               SQLCHAR *CatalogName, SQLSMALLINT NameLength1,
               SQLCHAR *SchemaName, SQLSMALLINT NameLength2,
               SQLCHAR *TableName, SQLSMALLINT NameLength3);
    SQLRETURN  SQLTables(SQLHSTMT StatementHandle,
               SQLCHAR *CatalogName, SQLSMALLINT NameLength1,
               SQLCHAR *SchemaName, SQLSMALLINT NameLength2,
               SQLCHAR *TableName, SQLSMALLINT NameLength3,
               SQLCHAR *TableType, SQLSMALLINT NameLength4 );
