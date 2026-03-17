# COBOL to Java Migration Notes

## Overview

| Item | Details |
|------|---------|
| **Source** | `customer-report.cbl` (COBOL) |
| **Target** | `CustomerReport.java` (Java 17+) |
| **Program** | CUSTOMER-REPORT — Customer Account Monthly Statement Report Generator |
| **Migration Date** | 2026-03-17 |

---

## Program Purpose

Reads customer master and transaction records from fixed-width flat files, calculates monthly balances with interest and fees, and generates a formatted monthly statement report.

---

## Structural Mapping

### COBOL Divisions → Java Equivalents

| COBOL Division / Section | Java Equivalent |
|--------------------------|-----------------|
| `IDENTIFICATION DIVISION` | Class-level Javadoc |
| `ENVIRONMENT DIVISION / FILE-CONTROL` | `static final String` file path constants |
| `DATA DIVISION / FILE SECTION` (FD records) | Inner classes `CustomerRecord`, `TransactionRecord` |
| `WORKING-STORAGE SECTION` | Instance fields and `static final` constants |
| `PROCEDURE DIVISION` (paragraphs) | Instance methods |

### COBOL Paragraphs → Java Methods

| COBOL Paragraph | Java Method | Notes |
|-----------------|-------------|-------|
| `0000-MAIN-PROCESS` | `run()` | Entry point loop |
| `1000-INITIALIZE` | `initialize()` | Opens files, reads all customers into a `List` |
| `2000-PROCESS-CUSTOMERS` | `processCustomer()` | Processes a single customer |
| `2100-INIT-CUSTOMER-ACCUMS` | `initCustomerAccums()` | Resets accumulators |
| `2200-PRINT-CUST-HEADER` | `printCustHeader()` | Writes customer header line |
| `2300-PROCESS-TRANSACTIONS` | `processTransactions()` | Loads and iterates transactions |
| `2310-PROCESS-SINGLE-TRAN` | _(inlined in loop)_ | Merged into `processTransactions()` |
| `2320-CATEGORIZE-TRANSACTION` | `categorizeTransaction()` | Accumulates by type |
| `2330-PRINT-DETAIL` | `printDetail()` | Writes transaction detail line |
| `2400-CALC-INTEREST` | `calcInterest()` | Monthly interest calculation |
| `2500-CALC-FEES` | `calcFees()` | Low-balance and overdraft fees |
| `2600-PRINT-SUMMARY` | `printSummary()` | Writes account summary block |
| `8000-PRINT-PAGE-HEADER` | `printPageHeader()` | Page break and header |
| `9000-FINALIZE` | `finalize_()` | Closes files, prints totals |

---

## Data Type Mappings

### Record Fields

| COBOL PIC | Java Type | Rationale |
|-----------|-----------|-----------|
| `PIC X(n)` | `String` | Alphanumeric text fields |
| `PIC X(1)` (with 88-levels) | `char` | Single-character codes compared against constants |
| `PIC 9(8)` | `String` | Date stored as `YYYYMMDD`, parsed as needed |
| `PIC 9(6)` | `String` | Time stored as `HHMMSS` |
| `PIC S9(9)V99` | `BigDecimal` | Signed decimal — monetary precision required |
| `PIC 9(n)` (counters) | `int` | Simple numeric counters |

### Why `BigDecimal`?

COBOL uses fixed-point decimal arithmetic natively. Java's `double`/`float` types introduce floating-point rounding errors that are unacceptable for financial calculations. `BigDecimal` preserves exact decimal precision, matching COBOL behavior.

---

## Constant Mappings

### 88-Level Condition Names → Java Constants

| COBOL 88-Level | Java Constant | Value |
|----------------|---------------|-------|
| `CHECKING` | `CHECKING` | `'C'` |
| `SAVINGS` | `SAVINGS` | `'S'` |
| `MONEY-MARKET` | `MONEY_MARKET` | `'M'` |
| `ACTIVE-ACCOUNT` | `ACTIVE` | `'A'` |
| `DEPOSIT` | `DEPOSIT` | `"DP"` |
| `WITHDRAWAL` | `WITHDRAWAL` | `"WD"` |
| `TRANSFER-IN` | `TRANSFER_IN` | `"TI"` |
| `TRANSFER-OUT` | `TRANSFER_OUT` | `"TO"` |
| `FEE` | `FEE` | `"FE"` |
| `INTEREST` | `INTEREST` | `"IN"` |
| `ADJUSTMENT` | `ADJUSTMENT` | `"AJ"` |

### Interest Rates (from `WS-INTEREST-RATES`)

| COBOL Field | Java Constant | Value |
|-------------|---------------|-------|
| `WS-CHECKING-RATE` | `CHECKING_RATE` | `0.0025` |
| `WS-SAVINGS-RATE` | `SAVINGS_RATE` | `0.0450` |
| `WS-MONEY-MKT-RATE` | `MONEY_MKT_RATE` | `0.0375` |

### Fee Schedule (from `WS-FEE-SCHEDULE`)

| COBOL Field | Java Constant | Value |
|-------------|---------------|-------|
| `WS-MONTHLY-FEE` | `MONTHLY_FEE` | `12.50` |
| `WS-OVERDRAFT-FEE` | `OVERDRAFT_FEE` | `35.00` |
| `WS-LOW-BAL-FEE` | `LOW_BAL_FEE` | `5.00` |
| `WS-MIN-BALANCE` | `MIN_BALANCE` | `500.00` |

---

## File I/O Mapping

### COBOL File Handling → Java I/O

| COBOL | Java |
|-------|------|
| `SELECT ... ASSIGN TO 'CUSTMAST.DAT'` | `private static final String CUSTOMER_FILE = "CUSTMAST.DAT"` |
| `OPEN INPUT CUSTOMER-FILE` | `new BufferedReader(new FileReader(CUSTOMER_FILE))` |
| `READ CUSTOMER-FILE AT END ...` | `reader.readLine()` with null check |
| `OPEN OUTPUT REPORT-FILE` | `new PrintWriter(new BufferedWriter(new FileWriter(REPORT_FILE)))` |
| `WRITE REPORT-LINE FROM ...` | `reportWriter.printf(...)` / `reportWriter.println(...)` |
| `CLOSE` | `reader.close()` (via try-with-resources) / `reportWriter.close()` |
| `FILE STATUS IS WS-CUST-STATUS` | `IOException` handling |

### Fixed-Width Record Parsing

COBOL reads fixed-width records directly into the `FD` record layout. In Java, each record class has a `parse(String line)` method that extracts fields by character position, mirroring the COBOL field widths:

- **Customer record**: 10 + 25 + 20 + 30 + 20 + 2 + 10 + 15 + 1 + 11 + 11 + 8 + 1 = 164 chars
- **Transaction record**: 10 + 8 + 6 + 2 + 11 + 40 + 12 = 89 chars

---

## Business Logic Preservation

### Interest Calculation (`2400-CALC-INTEREST`)

```
COBOL:  COMPUTE WS-TOTAL-INTEREST = WS-ENDING-BALANCE * (rate / 12)
        COMPUTE WS-TOTAL-INTEREST = FUNCTION INTEGER(WS-TOTAL-INTEREST * 100) / 100

Java:   totalInterest = endingBalance.multiply(rate)
            .divide(BigDecimal.valueOf(12), 2, RoundingMode.FLOOR);
```

The COBOL `FUNCTION INTEGER` truncates toward zero after scaling by 100, which is equivalent to `RoundingMode.FLOOR` for positive values. This preserves the truncation (not rounding) behavior of the original program.

### Fee Calculation (`2500-CALC-FEES`)

Two fee conditions preserved exactly:

1. **Low balance fee** ($5.00): Applied when account type is CHECKING and ending balance < $500.00 minimum
2. **Overdraft fee** ($35.00): Applied when ending balance < $0.00 (checked after low-balance fee)

Both fees are subtracted from the ending balance and added to the total fees accumulator, matching the COBOL logic order.

### Transaction Categorization (`2320-CATEGORIZE-TRANSACTION`)

The COBOL `EVALUATE TRUE` maps directly to a Java `switch` expression:

- `DP`, `TI` → added to `totalDeposits`
- `WD`, `TO` → added to `totalWithdrawals`
- `FE` → added to `totalFees`
- `IN` → added to `totalInterest`
- `AJ` → routed to deposits (positive) or withdrawals (negative)

### Net Change Calculation

```
COBOL:  COMPUTE WS-NET-CHANGE = WS-TOTAL-DEPOSITS
            + WS-TOTAL-WITHDRAWALS + WS-TOTAL-INTEREST - WS-TOTAL-FEES

Java:   netChange = totalDeposits.add(totalWithdrawals)
            .add(totalInterest).subtract(totalFees);
```

Note: Withdrawals are stored as negative values (signed), so adding them produces the correct net effect.

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Single-file design (no packages) | Mirrors the self-contained nature of the COBOL program; keeps the migration 1:1 |
| Inner classes for records | Equivalent to COBOL `FD` record definitions scoped within the program |
| `BigDecimal` throughout | Exact decimal math matching COBOL fixed-point arithmetic |
| `RoundingMode.FLOOR` for interest | Matches COBOL `FUNCTION INTEGER` truncation behavior |
| Transaction file re-read per customer | Mirrors COBOL's `CLOSE`/`OPEN`/`READ` loop per customer (paragraph 2300) |
| Java 17+ switch expressions | Clean translation of COBOL `EVALUATE TRUE` constructs |
| `PrintWriter.printf` for report output | Closest equivalent to COBOL formatted `WRITE` with `PIC` editing |

---

## Behavioral Differences to Be Aware Of

| Aspect | COBOL Behavior | Java Behavior |
|--------|----------------|---------------|
| **File access** | Sequential/indexed reads with `AT END` | All records loaded into `List` in memory |
| **Page breaks** | `AFTER ADVANCING PAGE` (printer control) | Extra newline printed (no physical page break) |
| **String handling** | Fixed-width, space-padded | Trimmed on output; `field()` utility preserves raw extraction |
| **Date source** | `ACCEPT FROM DATE YYYYMMDD` (system date) | `LocalDate.now()` |
| **Error handling** | `FILE STATUS` codes, `DISPLAY`, `STOP RUN` | `IOException`, `System.err`, `System.exit(1)` |
| **Numeric overflow** | COBOL silently truncates | `BigDecimal` has arbitrary precision (no overflow) |

---

## Testing Recommendations

1. **Create sample data files** (`CUSTMAST.DAT`, `TRANFILE.DAT`) with fixed-width records matching the field layouts above
2. **Verify interest calculations** — compare Java output against manual calculations using the same rates and `FLOOR` rounding
3. **Test fee edge cases** — checking account at exactly $500.00 (should NOT trigger low-balance fee) and at $499.99 (should trigger)
4. **Test overdraft cascading** — verify low-balance fee can push balance negative, triggering the overdraft fee
5. **Validate report formatting** — compare column alignment with expected COBOL report output
6. **Test with empty transaction file** — ensure no errors when a customer has zero transactions

---

## Future Improvement Opportunities

These were **not** done during migration to keep behavior identical to the COBOL original:

- Extract record parsing into a reusable file-format library
- Cache transactions instead of re-reading the file for each customer
- Add proper logging framework instead of `System.out`/`System.err`
- Move configuration (rates, fees, file paths) to external config
- Add unit tests with JUnit
- Consider migrating to a database instead of flat files
