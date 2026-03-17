import java.io.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * Customer Account Monthly Statement Report Generator.
 *
 * Converted from COBOL program CUSTOMER-REPORT.CBL.
 * Reads customer and transaction records, calculates monthly balances,
 * applies interest and fees, and generates a formatted monthly statement report.
 */
public class CustomerReport {

    // --- File paths (equivalent to COBOL SELECT/ASSIGN) ---
    private static final String CUSTOMER_FILE = "CUSTMAST.DAT";
    private static final String TRANSACTION_FILE = "TRANFILE.DAT";
    private static final String REPORT_FILE = "CUSTRPT.RPT";

    // --- Account type constants ---
    private static final char CHECKING = 'C';
    private static final char SAVINGS = 'S';
    private static final char MONEY_MARKET = 'M';

    // --- Account status constants ---
    private static final char ACTIVE = 'A';

    // --- Transaction type constants ---
    private static final String DEPOSIT = "DP";
    private static final String WITHDRAWAL = "WD";
    private static final String TRANSFER_IN = "TI";
    private static final String TRANSFER_OUT = "TO";
    private static final String FEE = "FE";
    private static final String INTEREST = "IN";
    private static final String ADJUSTMENT = "AJ";

    // --- Interest rates ---
    private static final BigDecimal CHECKING_RATE = new BigDecimal("0.0025");
    private static final BigDecimal SAVINGS_RATE = new BigDecimal("0.0450");
    private static final BigDecimal MONEY_MKT_RATE = new BigDecimal("0.0375");

    // --- Fee schedule ---
    private static final BigDecimal MONTHLY_FEE = new BigDecimal("12.50");
    private static final BigDecimal OVERDRAFT_FEE = new BigDecimal("35.00");
    private static final BigDecimal LOW_BAL_FEE = new BigDecimal("5.00");
    private static final BigDecimal MIN_BALANCE = new BigDecimal("500.00");

    // --- Report formatting ---
    private static final int LINES_PER_PAGE = 55;
    private static final int REPORT_WIDTH = 132;

    // --- Customer record (equivalent to COBOL FD CUSTOMER-FILE) ---
    static class CustomerRecord {
        String accountNum;      // PIC X(10)
        String lastName;        // PIC X(25)
        String firstName;       // PIC X(20)
        String street;          // PIC X(30)
        String city;            // PIC X(20)
        String state;           // PIC X(2)
        String zip;             // PIC X(10)
        String phone;           // PIC X(15)
        char accountType;       // PIC X(1)
        BigDecimal balance;     // PIC S9(9)V99
        BigDecimal creditLimit; // PIC S9(9)V99
        String openDate;        // PIC 9(8)
        char status;            // PIC X(1)

        static CustomerRecord parse(String line) {
            CustomerRecord rec = new CustomerRecord();
            // Fixed-width field parsing matching COBOL record layout
            int pos = 0;
            rec.accountNum = field(line, pos, pos + 10); pos += 10;
            rec.lastName   = field(line, pos, pos + 25); pos += 25;
            rec.firstName  = field(line, pos, pos + 20); pos += 20;
            rec.street     = field(line, pos, pos + 30); pos += 30;
            rec.city       = field(line, pos, pos + 20); pos += 20;
            rec.state      = field(line, pos, pos + 2);  pos += 2;
            rec.zip        = field(line, pos, pos + 10); pos += 10;
            rec.phone      = field(line, pos, pos + 15); pos += 15;
            rec.accountType = line.charAt(pos);          pos += 1;
            rec.balance     = parsePic9(line, pos, 11);  pos += 11;
            rec.creditLimit = parsePic9(line, pos, 11);  pos += 11;
            rec.openDate    = field(line, pos, pos + 8); pos += 8;
            rec.status      = line.charAt(pos);
            return rec;
        }
    }

    // --- Transaction record (equivalent to COBOL FD TRANSACTION-FILE) ---
    static class TransactionRecord {
        String accountNum;   // PIC X(10)
        String date;         // PIC 9(8)
        String time;         // PIC 9(6)
        String type;         // PIC X(2)
        BigDecimal amount;   // PIC S9(9)V99
        String description;  // PIC X(40)
        String refNum;       // PIC X(12)

        static TransactionRecord parse(String line) {
            TransactionRecord rec = new TransactionRecord();
            int pos = 0;
            rec.accountNum  = field(line, pos, pos + 10); pos += 10;
            rec.date        = field(line, pos, pos + 8);  pos += 8;
            rec.time        = field(line, pos, pos + 6);  pos += 6;
            rec.type        = field(line, pos, pos + 2);  pos += 2;
            rec.amount      = parsePic9(line, pos, 11);   pos += 11;
            rec.description = field(line, pos, pos + 40); pos += 40;
            rec.refNum      = field(line, pos, pos + 12);
            return rec;
        }
    }

    // --- Working storage accumulators ---
    private BigDecimal totalDeposits;
    private BigDecimal totalWithdrawals;
    private BigDecimal totalFees;
    private BigDecimal totalInterest;
    private BigDecimal netChange;
    private BigDecimal endingBalance;

    // --- Counters ---
    private int custCount;
    private int tranCount;
    private int pageNum;
    private int lineNum;

    // --- Current date ---
    private LocalDate currentDate;

    // --- Report writer ---
    private PrintWriter reportWriter;

    // --- Main entry point ---
    public static void main(String[] args) {
        new CustomerReport().run();
    }

    /** 0000-MAIN-PROCESS */
    public void run() {
        List<CustomerRecord> customers = initialize();
        for (CustomerRecord customer : customers) {
            processCustomer(customer);
        }
        finalize_();
    }

    /** 1000-INITIALIZE */
    private List<CustomerRecord> initialize() {
        currentDate = LocalDate.now();
        custCount = 0;
        tranCount = 0;
        pageNum = 0;
        lineNum = 99; // Forces first page header

        List<CustomerRecord> customers = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(CUSTOMER_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.isEmpty()) {
                    customers.add(CustomerRecord.parse(line));
                }
            }
        } catch (IOException e) {
            System.err.println("ERROR OPENING CUSTOMER FILE: " + e.getMessage());
            System.exit(1);
        }

        try {
            reportWriter = new PrintWriter(new BufferedWriter(new FileWriter(REPORT_FILE)));
        } catch (IOException e) {
            System.err.println("ERROR OPENING REPORT FILE: " + e.getMessage());
            System.exit(1);
        }

        return customers;
    }

    /** 2000-PROCESS-CUSTOMERS */
    private void processCustomer(CustomerRecord customer) {
        if (customer.status != ACTIVE) {
            return;
        }
        custCount++;
        initCustomerAccums(customer);
        printCustHeader(customer);
        processTransactions(customer);
        calcInterest(customer);
        calcFees(customer);
        printSummary();
    }

    /** 2100-INIT-CUSTOMER-ACCUMS */
    private void initCustomerAccums(CustomerRecord customer) {
        totalDeposits = BigDecimal.ZERO;
        totalWithdrawals = BigDecimal.ZERO;
        totalFees = BigDecimal.ZERO;
        totalInterest = BigDecimal.ZERO;
        endingBalance = customer.balance;
    }

    /** 2200-PRINT-CUST-HEADER */
    private void printCustHeader(CustomerRecord customer) {
        if (lineNum > LINES_PER_PAGE) {
            printPageHeader();
        }
        String name = customer.firstName.trim() + " " + customer.lastName.trim();
        String typeName = switch (customer.accountType) {
            case CHECKING -> "CHECKING";
            case SAVINGS -> "SAVINGS";
            case MONEY_MARKET -> "MONEY MARKET";
            default -> "UNKNOWN";
        };
        reportWriter.printf("Account: %-10s  Name: %-46s  Type: %-15s%n",
                customer.accountNum.trim(), name, typeName);
        lineNum++;
    }

    /** 2300-PROCESS-TRANSACTIONS */
    private void processTransactions(CustomerRecord customer) {
        List<TransactionRecord> transactions = loadTransactions();
        for (TransactionRecord tran : transactions) {
            if (tran.accountNum.equals(customer.accountNum)) {
                tranCount++;
                categorizeTransaction(tran);
                endingBalance = endingBalance.add(tran.amount);
                printDetail(tran);
            }
        }
    }

    /** Load all transactions from file */
    private List<TransactionRecord> loadTransactions() {
        List<TransactionRecord> transactions = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(TRANSACTION_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.isEmpty()) {
                    transactions.add(TransactionRecord.parse(line));
                }
            }
        } catch (IOException e) {
            System.err.println("ERROR READING TRANSACTION FILE: " + e.getMessage());
        }
        return transactions;
    }

    /** 2320-CATEGORIZE-TRANSACTION */
    private void categorizeTransaction(TransactionRecord tran) {
        switch (tran.type.trim()) {
            case DEPOSIT, TRANSFER_IN ->
                    totalDeposits = totalDeposits.add(tran.amount);
            case WITHDRAWAL, TRANSFER_OUT ->
                    totalWithdrawals = totalWithdrawals.add(tran.amount);
            case FEE ->
                    totalFees = totalFees.add(tran.amount);
            case INTEREST ->
                    totalInterest = totalInterest.add(tran.amount);
            case ADJUSTMENT -> {
                if (tran.amount.compareTo(BigDecimal.ZERO) > 0) {
                    totalDeposits = totalDeposits.add(tran.amount);
                } else {
                    totalWithdrawals = totalWithdrawals.add(tran.amount);
                }
            }
        }
    }

    /** 2330-PRINT-DETAIL */
    private void printDetail(TransactionRecord tran) {
        if (lineNum > LINES_PER_PAGE) {
            printPageHeader();
        }
        // Format date from YYYYMMDD to MM/DD/YYYY
        String formattedDate = tran.date.substring(4, 6) + "/"
                + tran.date.substring(6, 8) + "/"
                + tran.date.substring(0, 4);

        String typeName = switch (tran.type.trim()) {
            case DEPOSIT -> "DEPOSIT";
            case WITHDRAWAL -> "WITHDRAWAL";
            case TRANSFER_IN -> "TRANSFER IN";
            case TRANSFER_OUT -> "TRANSFER OUT";
            case FEE -> "FEE";
            case INTEREST -> "INTEREST";
            case ADJUSTMENT -> "ADJUSTMENT";
            default -> tran.type;
        };

        reportWriter.printf("%-10s   %-15s   %-40s   %12.2f   %12.2f%n",
                formattedDate, typeName, tran.description.trim(),
                tran.amount, endingBalance);
        lineNum++;
    }

    /** 2400-CALC-INTEREST */
    private void calcInterest(CustomerRecord customer) {
        BigDecimal rate = switch (customer.accountType) {
            case CHECKING -> CHECKING_RATE;
            case SAVINGS -> SAVINGS_RATE;
            case MONEY_MARKET -> MONEY_MKT_RATE;
            default -> BigDecimal.ZERO;
        };

        totalInterest = endingBalance.multiply(rate)
                .divide(BigDecimal.valueOf(12), 2, RoundingMode.FLOOR);
        endingBalance = endingBalance.add(totalInterest);
    }

    /** 2500-CALC-FEES */
    private void calcFees(CustomerRecord customer) {
        if (customer.accountType == CHECKING
                && endingBalance.compareTo(MIN_BALANCE) < 0) {
            endingBalance = endingBalance.subtract(LOW_BAL_FEE);
            totalFees = totalFees.add(LOW_BAL_FEE);
        }
        if (endingBalance.compareTo(BigDecimal.ZERO) < 0) {
            endingBalance = endingBalance.subtract(OVERDRAFT_FEE);
            totalFees = totalFees.add(OVERDRAFT_FEE);
        }
    }

    /** 2600-PRINT-SUMMARY */
    private void printSummary() {
        reportWriter.println();
        reportWriter.printf("%40s%-25s%n", "", "-------------------------");
        reportWriter.printf("%40s%-25s%13.2f%n", "", "Total Deposits:", totalDeposits);
        reportWriter.printf("%40s%-25s%13.2f%n", "", "Total Withdrawals:", totalWithdrawals);
        reportWriter.printf("%40s%-25s%13.2f%n", "", "Interest Earned:", totalInterest);
        reportWriter.printf("%40s%-25s%13.2f%n", "", "Fees Charged:", totalFees);

        netChange = totalDeposits.add(totalWithdrawals)
                .add(totalInterest).subtract(totalFees);
        reportWriter.printf("%40s%-25s%13.2f%n", "", "Net Change:", netChange);
        reportWriter.printf("%40s%-25s%13.2f%n", "", "Ending Balance:", endingBalance);
        lineNum += 8;
    }

    /** 8000-PRINT-PAGE-HEADER */
    private void printPageHeader() {
        pageNum++;
        String dateStr = String.format("%02d/%02d/%04d",
                currentDate.getMonthValue(), currentDate.getDayOfMonth(), currentDate.getYear());

        reportWriter.println();
        reportWriter.println("========================================" +
                "  MONTHLY ACCOUNT STATEMENT     " +
                "========================================");
        reportWriter.printf("Statement Date: %-10s%60sPage %,5d%n",
                dateStr, "", pageNum);
        reportWriter.println();
        lineNum = 4;
    }

    /** 9000-FINALIZE */
    private void finalize_() {
        if (reportWriter != null) {
            reportWriter.close();
        }
        System.out.println("REPORT COMPLETE");
        System.out.println("CUSTOMERS PROCESSED: " + custCount);
        System.out.println("TRANSACTIONS PROCESSED: " + tranCount);
    }

    // --- Utility methods ---

    /** Extract and trim a fixed-width field from a line */
    private static String field(String line, int start, int end) {
        if (line.length() < end) {
            return line.substring(start).trim();
        }
        return line.substring(start, end);
    }

    /** Parse a COBOL-style signed decimal (PIC S9(9)V99) from fixed-width text */
    private static BigDecimal parsePic9(String line, int start, int length) {
        String raw = field(line, start, start + length).trim();
        if (raw.isEmpty()) {
            return BigDecimal.ZERO;
        }
        try {
            return new BigDecimal(raw);
        } catch (NumberFormatException e) {
            return BigDecimal.ZERO;
        }
    }
}
