      ******************************************************************
      * CUSTOMER-REPORT.CBL
      * Customer Account Monthly Statement Report Generator
      *
      * This COBOL program reads customer and transaction records,
      * calculates monthly balances, applies interest and fees,
      * and generates a formatted monthly statement report.
      *
      * DEMO INSTRUCTIONS:
      * ==================
      * 1. Open this file and ask Copilot Chat:
      *    "Convert this COBOL program to Java"
      * 2. Watch Copilot translate the entire program including:
      *    - Data structures → Java classes
      *    - Paragraph logic → Methods
      *    - File I/O → Java file handling
      *    - Report formatting → String formatting
      * 3. Follow up with: "Add unit tests for the Java version"
      * 4. Discuss with audience: This is a STARTING POINT, not a
      *    push-button migration (see Scenario 1 discussion guide)
      ******************************************************************

       IDENTIFICATION DIVISION.
       PROGRAM-ID. CUSTOMER-REPORT.
       AUTHOR. DEMO-TEAM.
       DATE-WRITTEN. 2024-01-15.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CUSTOMER-FILE
               ASSIGN TO 'CUSTMAST.DAT'
               ORGANIZATION IS INDEXED
               ACCESS MODE IS SEQUENTIAL
               RECORD KEY IS CUST-ACCOUNT-NUM
               FILE STATUS IS WS-CUST-STATUS.

           SELECT TRANSACTION-FILE
               ASSIGN TO 'TRANFILE.DAT'
               ORGANIZATION IS SEQUENTIAL
               FILE STATUS IS WS-TRAN-STATUS.

           SELECT REPORT-FILE
               ASSIGN TO 'CUSTRPT.RPT'
               ORGANIZATION IS SEQUENTIAL
               FILE STATUS IS WS-RPT-STATUS.

       DATA DIVISION.
       FILE SECTION.

       FD  CUSTOMER-FILE.
       01  CUSTOMER-RECORD.
           05  CUST-ACCOUNT-NUM       PIC X(10).
           05  CUST-NAME.
               10  CUST-LAST-NAME     PIC X(25).
               10  CUST-FIRST-NAME    PIC X(20).
           05  CUST-ADDRESS.
               10  CUST-STREET        PIC X(30).
               10  CUST-CITY          PIC X(20).
               10  CUST-STATE         PIC X(2).
               10  CUST-ZIP           PIC X(10).
           05  CUST-PHONE             PIC X(15).
           05  CUST-ACCOUNT-TYPE      PIC X(1).
               88  CHECKING           VALUE 'C'.
               88  SAVINGS            VALUE 'S'.
               88  MONEY-MARKET       VALUE 'M'.
           05  CUST-BALANCE           PIC S9(9)V99.
           05  CUST-CREDIT-LIMIT      PIC S9(9)V99.
           05  CUST-OPEN-DATE         PIC 9(8).
           05  CUST-STATUS            PIC X(1).
               88  ACTIVE-ACCOUNT     VALUE 'A'.
               88  CLOSED-ACCOUNT     VALUE 'C'.
               88  SUSPENDED-ACCOUNT  VALUE 'S'.

       FD  TRANSACTION-FILE.
       01  TRANSACTION-RECORD.
           05  TRAN-ACCOUNT-NUM       PIC X(10).
           05  TRAN-DATE              PIC 9(8).
           05  TRAN-TIME              PIC 9(6).
           05  TRAN-TYPE              PIC X(2).
               88  DEPOSIT            VALUE 'DP'.
               88  WITHDRAWAL         VALUE 'WD'.
               88  TRANSFER-IN        VALUE 'TI'.
               88  TRANSFER-OUT       VALUE 'TO'.
               88  FEE                VALUE 'FE'.
               88  INTEREST           VALUE 'IN'.
               88  ADJUSTMENT         VALUE 'AJ'.
           05  TRAN-AMOUNT            PIC S9(9)V99.
           05  TRAN-DESCRIPTION       PIC X(40).
           05  TRAN-REF-NUM           PIC X(12).

       FD  REPORT-FILE.
       01  REPORT-LINE                PIC X(132).

       WORKING-STORAGE SECTION.

       01  WS-FILE-STATUS.
           05  WS-CUST-STATUS         PIC XX.
           05  WS-TRAN-STATUS         PIC XX.
           05  WS-RPT-STATUS          PIC XX.

       01  WS-FLAGS.
           05  WS-EOF-CUST            PIC X    VALUE 'N'.
               88  END-OF-CUSTOMERS   VALUE 'Y'.
           05  WS-EOF-TRAN            PIC X    VALUE 'N'.
               88  END-OF-TRANS       VALUE 'Y'.

       01  WS-COUNTERS.
           05  WS-CUST-COUNT          PIC 9(6) VALUE 0.
           05  WS-TRAN-COUNT          PIC 9(8) VALUE 0.
           05  WS-PAGE-NUM            PIC 9(4) VALUE 0.
           05  WS-LINE-NUM            PIC 9(2) VALUE 99.
           05  WS-LINES-PER-PAGE      PIC 9(2) VALUE 55.

       01  WS-ACCUMULATORS.
           05  WS-TOTAL-DEPOSITS      PIC S9(11)V99 VALUE 0.
           05  WS-TOTAL-WITHDRAWALS   PIC S9(11)V99 VALUE 0.
           05  WS-TOTAL-FEES          PIC S9(11)V99 VALUE 0.
           05  WS-TOTAL-INTEREST      PIC S9(11)V99 VALUE 0.
           05  WS-NET-CHANGE          PIC S9(11)V99 VALUE 0.
           05  WS-ENDING-BALANCE      PIC S9(11)V99 VALUE 0.

       01  WS-INTEREST-RATES.
           05  WS-CHECKING-RATE       PIC 9V9(4) VALUE 0.0025.
           05  WS-SAVINGS-RATE        PIC 9V9(4) VALUE 0.0450.
           05  WS-MONEY-MKT-RATE      PIC 9V9(4) VALUE 0.0375.

       01  WS-FEE-SCHEDULE.
           05  WS-MONTHLY-FEE         PIC 9(3)V99  VALUE 12.50.
           05  WS-OVERDRAFT-FEE       PIC 9(3)V99  VALUE 35.00.
           05  WS-LOW-BAL-FEE         PIC 9(3)V99  VALUE 5.00.
           05  WS-MIN-BALANCE         PIC 9(7)V99  VALUE 500.00.

       01  WS-CURRENT-DATE.
           05  WS-CURR-YEAR           PIC 9(4).
           05  WS-CURR-MONTH          PIC 9(2).
           05  WS-CURR-DAY            PIC 9(2).

       01  WS-REPORT-HEADER-1.
           05  FILLER                 PIC X(40)
               VALUE '========================================'.
           05  FILLER                 PIC X(32)
               VALUE '  MONTHLY ACCOUNT STATEMENT     '.
           05  FILLER                 PIC X(40)
               VALUE '========================================'.

       01  WS-REPORT-HEADER-2.
           05  FILLER                 PIC X(15) VALUE 'Statement Date:'.
           05  WS-HDR-DATE            PIC X(10).
           05  FILLER                 PIC X(60) VALUE SPACES.
           05  FILLER                 PIC X(5)  VALUE 'Page '.
           05  WS-HDR-PAGE            PIC Z,ZZ9.

       01  WS-CUST-HEADER.
           05  FILLER                 PIC X(9)  VALUE 'Account: '.
           05  WS-CH-ACCT             PIC X(10).
           05  FILLER                 PIC X(8)  VALUE '  Name: '.
           05  WS-CH-NAME             PIC X(46).
           05  FILLER                 PIC X(7)  VALUE '  Type: '.
           05  WS-CH-TYPE             PIC X(15).

       01  WS-DETAIL-LINE.
           05  WS-DL-DATE             PIC X(10).
           05  FILLER                 PIC X(3)  VALUE SPACES.
           05  WS-DL-TYPE             PIC X(15).
           05  FILLER                 PIC X(3)  VALUE SPACES.
           05  WS-DL-DESC             PIC X(40).
           05  FILLER                 PIC X(3)  VALUE SPACES.
           05  WS-DL-AMOUNT           PIC -(9)9.99.
           05  FILLER                 PIC X(3)  VALUE SPACES.
           05  WS-DL-BALANCE          PIC -(9)9.99.

       01  WS-SUMMARY-LINE.
           05  FILLER                 PIC X(40) VALUE SPACES.
           05  WS-SL-LABEL            PIC X(25).
           05  WS-SL-AMOUNT           PIC -(11)9.99.

       PROCEDURE DIVISION.

       0000-MAIN-PROCESS.
           PERFORM 1000-INITIALIZE
           PERFORM 2000-PROCESS-CUSTOMERS
               UNTIL END-OF-CUSTOMERS
           PERFORM 9000-FINALIZE
           STOP RUN.

       1000-INITIALIZE.
           ACCEPT WS-CURRENT-DATE FROM DATE YYYYMMDD
           OPEN INPUT  CUSTOMER-FILE
                INPUT  TRANSACTION-FILE
                OUTPUT REPORT-FILE
           IF WS-CUST-STATUS NOT = '00'
               DISPLAY 'ERROR OPENING CUSTOMER FILE: ' WS-CUST-STATUS
               STOP RUN
           END-IF
           READ CUSTOMER-FILE
               AT END SET END-OF-CUSTOMERS TO TRUE
           END-READ.

       2000-PROCESS-CUSTOMERS.
           IF ACTIVE-ACCOUNT
               ADD 1 TO WS-CUST-COUNT
               PERFORM 2100-INIT-CUSTOMER-ACCUMS
               PERFORM 2200-PRINT-CUST-HEADER
               PERFORM 2300-PROCESS-TRANSACTIONS
               PERFORM 2400-CALC-INTEREST
               PERFORM 2500-CALC-FEES
               PERFORM 2600-PRINT-SUMMARY
           END-IF
           READ CUSTOMER-FILE
               AT END SET END-OF-CUSTOMERS TO TRUE
           END-READ.

       2100-INIT-CUSTOMER-ACCUMS.
           MOVE 0 TO WS-TOTAL-DEPOSITS
           MOVE 0 TO WS-TOTAL-WITHDRAWALS
           MOVE 0 TO WS-TOTAL-FEES
           MOVE 0 TO WS-TOTAL-INTEREST
           MOVE CUST-BALANCE TO WS-ENDING-BALANCE.

       2200-PRINT-CUST-HEADER.
           IF WS-LINE-NUM > WS-LINES-PER-PAGE
               PERFORM 8000-PRINT-PAGE-HEADER
           END-IF
           MOVE CUST-ACCOUNT-NUM TO WS-CH-ACCT
           STRING CUST-FIRST-NAME DELIMITED BY '  '
                  ' ' DELIMITED BY SIZE
                  CUST-LAST-NAME DELIMITED BY '  '
                  INTO WS-CH-NAME
           EVALUATE TRUE
               WHEN CHECKING
                   MOVE 'CHECKING' TO WS-CH-TYPE
               WHEN SAVINGS
                   MOVE 'SAVINGS' TO WS-CH-TYPE
               WHEN MONEY-MARKET
                   MOVE 'MONEY MARKET' TO WS-CH-TYPE
           END-EVALUATE
           WRITE REPORT-LINE FROM WS-CUST-HEADER
           ADD 1 TO WS-LINE-NUM.

       2300-PROCESS-TRANSACTIONS.
           MOVE 'N' TO WS-EOF-TRAN
           CLOSE TRANSACTION-FILE
           OPEN INPUT TRANSACTION-FILE
           READ TRANSACTION-FILE
               AT END SET END-OF-TRANS TO TRUE
           END-READ
           PERFORM 2310-PROCESS-SINGLE-TRAN
               UNTIL END-OF-TRANS.

       2310-PROCESS-SINGLE-TRAN.
           IF TRAN-ACCOUNT-NUM = CUST-ACCOUNT-NUM
               ADD 1 TO WS-TRAN-COUNT
               PERFORM 2320-CATEGORIZE-TRANSACTION
               PERFORM 2330-PRINT-DETAIL
               COMPUTE WS-ENDING-BALANCE =
                   WS-ENDING-BALANCE + TRAN-AMOUNT
           END-IF
           READ TRANSACTION-FILE
               AT END SET END-OF-TRANS TO TRUE
           END-READ.

       2320-CATEGORIZE-TRANSACTION.
           EVALUATE TRUE
               WHEN DEPOSIT
               WHEN TRANSFER-IN
                   ADD TRAN-AMOUNT TO WS-TOTAL-DEPOSITS
               WHEN WITHDRAWAL
               WHEN TRANSFER-OUT
                   ADD TRAN-AMOUNT TO WS-TOTAL-WITHDRAWALS
               WHEN FEE
                   ADD TRAN-AMOUNT TO WS-TOTAL-FEES
               WHEN INTEREST
                   ADD TRAN-AMOUNT TO WS-TOTAL-INTEREST
               WHEN ADJUSTMENT
                   IF TRAN-AMOUNT > 0
                       ADD TRAN-AMOUNT TO WS-TOTAL-DEPOSITS
                   ELSE
                       ADD TRAN-AMOUNT TO WS-TOTAL-WITHDRAWALS
                   END-IF
           END-EVALUATE.

       2330-PRINT-DETAIL.
           IF WS-LINE-NUM > WS-LINES-PER-PAGE
               PERFORM 8000-PRINT-PAGE-HEADER
           END-IF
           STRING TRAN-DATE(5:2) '/' TRAN-DATE(7:2) '/'
                  TRAN-DATE(1:4) DELIMITED BY SIZE
                  INTO WS-DL-DATE
           EVALUATE TRUE
               WHEN DEPOSIT       MOVE 'DEPOSIT' TO WS-DL-TYPE
               WHEN WITHDRAWAL    MOVE 'WITHDRAWAL' TO WS-DL-TYPE
               WHEN TRANSFER-IN   MOVE 'TRANSFER IN' TO WS-DL-TYPE
               WHEN TRANSFER-OUT  MOVE 'TRANSFER OUT' TO WS-DL-TYPE
               WHEN FEE           MOVE 'FEE' TO WS-DL-TYPE
               WHEN INTEREST      MOVE 'INTEREST' TO WS-DL-TYPE
               WHEN ADJUSTMENT    MOVE 'ADJUSTMENT' TO WS-DL-TYPE
           END-EVALUATE
           MOVE TRAN-DESCRIPTION TO WS-DL-DESC
           MOVE TRAN-AMOUNT TO WS-DL-AMOUNT
           MOVE WS-ENDING-BALANCE TO WS-DL-BALANCE
           WRITE REPORT-LINE FROM WS-DETAIL-LINE
           ADD 1 TO WS-LINE-NUM.

       2400-CALC-INTEREST.
           EVALUATE TRUE
               WHEN CHECKING
                   COMPUTE WS-TOTAL-INTEREST =
                       WS-ENDING-BALANCE *
                       (WS-CHECKING-RATE / 12)
               WHEN SAVINGS
                   COMPUTE WS-TOTAL-INTEREST =
                       WS-ENDING-BALANCE *
                       (WS-SAVINGS-RATE / 12)
               WHEN MONEY-MARKET
                   COMPUTE WS-TOTAL-INTEREST =
                       WS-ENDING-BALANCE *
                       (WS-MONEY-MKT-RATE / 12)
           END-EVALUATE
           COMPUTE WS-TOTAL-INTEREST =
               FUNCTION INTEGER(WS-TOTAL-INTEREST * 100) / 100
           ADD WS-TOTAL-INTEREST TO WS-ENDING-BALANCE.

       2500-CALC-FEES.
           IF CHECKING AND WS-ENDING-BALANCE < WS-MIN-BALANCE
               SUBTRACT WS-LOW-BAL-FEE FROM WS-ENDING-BALANCE
               ADD WS-LOW-BAL-FEE TO WS-TOTAL-FEES
           END-IF
           IF WS-ENDING-BALANCE < 0
               SUBTRACT WS-OVERDRAFT-FEE FROM WS-ENDING-BALANCE
               ADD WS-OVERDRAFT-FEE TO WS-TOTAL-FEES
           END-IF.

       2600-PRINT-SUMMARY.
           MOVE SPACES TO REPORT-LINE
           WRITE REPORT-LINE
           MOVE '-------------------------' TO WS-SL-LABEL
           MOVE WS-SL-LABEL TO REPORT-LINE
           WRITE REPORT-LINE

           MOVE 'Total Deposits:' TO WS-SL-LABEL
           MOVE WS-TOTAL-DEPOSITS TO WS-SL-AMOUNT
           WRITE REPORT-LINE FROM WS-SUMMARY-LINE

           MOVE 'Total Withdrawals:' TO WS-SL-LABEL
           MOVE WS-TOTAL-WITHDRAWALS TO WS-SL-AMOUNT
           WRITE REPORT-LINE FROM WS-SUMMARY-LINE

           MOVE 'Interest Earned:' TO WS-SL-LABEL
           MOVE WS-TOTAL-INTEREST TO WS-SL-AMOUNT
           WRITE REPORT-LINE FROM WS-SUMMARY-LINE

           MOVE 'Fees Charged:' TO WS-SL-LABEL
           MOVE WS-TOTAL-FEES TO WS-SL-AMOUNT
           WRITE REPORT-LINE FROM WS-SUMMARY-LINE

           COMPUTE WS-NET-CHANGE = WS-TOTAL-DEPOSITS
               + WS-TOTAL-WITHDRAWALS + WS-TOTAL-INTEREST
               - WS-TOTAL-FEES
           MOVE 'Net Change:' TO WS-SL-LABEL
           MOVE WS-NET-CHANGE TO WS-SL-AMOUNT
           WRITE REPORT-LINE FROM WS-SUMMARY-LINE

           MOVE 'Ending Balance:' TO WS-SL-LABEL
           MOVE WS-ENDING-BALANCE TO WS-SL-AMOUNT
           WRITE REPORT-LINE FROM WS-SUMMARY-LINE

           ADD 8 TO WS-LINE-NUM.

       8000-PRINT-PAGE-HEADER.
           ADD 1 TO WS-PAGE-NUM
           MOVE WS-PAGE-NUM TO WS-HDR-PAGE
           STRING WS-CURR-MONTH '/' WS-CURR-DAY '/'
                  WS-CURR-YEAR DELIMITED BY SIZE
                  INTO WS-HDR-DATE
           WRITE REPORT-LINE FROM WS-REPORT-HEADER-1
               AFTER ADVANCING PAGE
           WRITE REPORT-LINE FROM WS-REPORT-HEADER-2
           MOVE SPACES TO REPORT-LINE
           WRITE REPORT-LINE
           MOVE 4 TO WS-LINE-NUM.

       9000-FINALIZE.
           CLOSE CUSTOMER-FILE
                 TRANSACTION-FILE
                 REPORT-FILE
           DISPLAY 'REPORT COMPLETE'
           DISPLAY 'CUSTOMERS PROCESSED: ' WS-CUST-COUNT
           DISPLAY 'TRANSACTIONS PROCESSED: ' WS-TRAN-COUNT.
