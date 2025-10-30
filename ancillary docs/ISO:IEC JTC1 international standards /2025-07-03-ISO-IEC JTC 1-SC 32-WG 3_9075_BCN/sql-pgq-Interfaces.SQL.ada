
-- The following lines of Ada code are intended to be inserted into the Ada package
-- Interfaces.SQL that is defined in ISO/IEC 9075-2. 

-- They should be inserted immediately following the line that reads:
--   package SQLSTATE_CODES is

    DATA_EXCEPTION_NO_SUBCLASS:
      constant SQLSTATE_TYPE := "22000";
    DATA_EXCEPTION_INVALID_NUMBER_OF_PATHS_OR_GROUPS:
      constant SQLSTATE_TYPE := "22G0F";
    DATA_EXCEPTION_MULTI_SOURCED_OR_MULTI_DESTINED_EDGE:
      constant SQLSTATE_TYPE := "22G0K";
    DATA_EXCEPTION_INCOMPLETE_EDGE:
      constant SQLSTATE_TYPE := "22G0L";
