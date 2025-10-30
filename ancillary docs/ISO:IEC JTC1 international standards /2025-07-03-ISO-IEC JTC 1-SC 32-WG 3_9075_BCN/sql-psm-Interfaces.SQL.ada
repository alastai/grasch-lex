
-- The following lines of Ada code are intended to be inserted into the Ada package
-- Interfaces.SQL that is defined in ISO/IEC 9075-2. 

-- They should be inserted immediately following the line that reads:
--   package SQLSTATE_CODES is

    RESIGNAL_WHEN_HANDLER_NOT_ACTIVE_NO_SUBCLASS:
      constant SQLSTATE_TYPE := "0K000";
    DIAGNOSTICS_EXCEPTION_NO_SUBCLASS:
      constant SQLSTATE_TYPE := "0Z000";
    DIAGNOSTICS_EXCEPTION_STACKED_DIAGNOSTICS_ACCESSED_WITHOUT_ACTIVE_HANDLER:
      constant SQLSTATE_TYPE := "0Z002";
    CASE_NOT_FOUND_FOR_CASE_STATEMENT_NO_SUBCLASS:
      constant SQLSTATE_TYPE := "20000";
    DATA_EXCEPTION_NO_SUBCLASS:
      constant SQLSTATE_TYPE := "22000";
    DATA_EXCEPTION_NULL_VALUE_IN_FIELD_REFERENCE:
      constant SQLSTATE_TYPE := "2202A";
    UNHANDLED_USER_DEFINED_EXCEPTION_NO_SUBCLASS:
      constant SQLSTATE_TYPE := "45000";
