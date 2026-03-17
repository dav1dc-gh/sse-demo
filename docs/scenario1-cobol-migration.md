# Scenario 1: COBOL-to-Java Migration at Scale

## The Customer's Situation
> "We have millions of lines of COBOL code. We want to use Copilot to convert
> all that code into Java so we can more easily find talented developers."

---

## Key Talking Points

### What Copilot CAN Do (Demo This Live!)
- **Translate individual programs**: Copilot excels at converting discrete COBOL
  programs, paragraphs, and copybooks into well-structured Java classes
- **Understand COBOL idioms**: It recognizes COBOL-specific patterns (EVALUATE,
  PERFORM VARYING, REDEFINES, 88-level conditions) and maps them to Java equivalents
- **Preserve business logic**: Copilot understands the *intent* of the code, not
  just the syntax — it produces idiomatic Java, not a line-by-line transliteration
- **Generate tests**: After conversion, Copilot can generate unit tests for the
  Java output, helping validate that the conversion is correct
- **Explain legacy code**: Even before conversion, Copilot Chat can explain what
  a COBOL program does, making it accessible to developers who don't know COBOL

### What the Customer Needs to Understand

#### 1. Copilot Is an Accelerator, Not a Replacement for a Migration Strategy
- Converting millions of lines of COBOL is a **major enterprise modernization program**,
  not a "run it through a tool" exercise
- Copilot dramatically accelerates the *conversion work* — what might take a developer
  a week per program can be done in hours — but the surrounding concerns remain:
  - **Data migration** (VSAM/DB2 → modern databases)
  - **Integration testing** (JCL batch flows, CICS transactions, MQ interfaces)
  - **Operational parity** (batch scheduling, error handling, monitoring)
  - **Performance validation** (COBOL on mainframes is *extremely* optimized)

#### 2. A Phased, Program-by-Program Approach Is Recommended
- Don't attempt a "big bang" conversion of all COBOL at once
- **Strangler Fig Pattern**: Convert one program/service at a time, run in parallel
  with the mainframe, validate, then cut over
- Copilot is ideal for this: developer opens a COBOL program, uses Chat to understand
  it, converts it to Java, generates tests, iterates — repeat for the next program

#### 3. The "Talented Developers" Angle Is the Real Win
- The customer's stated goal — finding developers — is actually the strongest
  argument for using Copilot *regardless* of the COBOL migration
- Even developers who stay in COBOL can use Copilot to:
  - Understand unfamiliar COBOL programs faster
  - Generate COBOL code (yes, Copilot knows COBOL!)
  - Write documentation for legacy systems
- For new Java code, Copilot makes Java developers **significantly more productive**

#### 4. Consider a Hybrid Approach
- Not all COBOL *needs* to be converted — some batch programs that run fine on
  the mainframe can stay there
- Use Copilot to build **new Java services** that integrate with existing COBOL
  programs via APIs, message queues, or shared databases
- Prioritize conversion for programs that:
  - Change frequently (high maintenance cost)
  - Need new features that are hard to build in COBOL
  - Have compliance/security requirements that benefit from modern tooling

### Potential Objections and Responses

| Objection | Response |
|-----------|----------|
| "Can't we just batch-convert everything?" | Conversion is the easy part. Validation, testing, and operational readiness are 70% of the effort. Copilot accelerates the conversion piece enormously. |
| "How accurate is the conversion?" | Very good for business logic translation, but every conversion needs human review and testing — just like code from any developer. |
| "We tried automated COBOL converters before and they produced unreadable code" | Copilot generates *idiomatic* Java, not a 1:1 transliteration. It understands both languages natively. Live demo shows this clearly. |
| "How long will the full migration take?" | That depends on complexity, but Copilot can reduce the per-program conversion effort by 50-70%. The rest is testing and integration work. |

### Live Demo Script (for this scenario)
1. Open `demos/07-cobol-to-java/customer-report.cbl`
2. Ask Copilot Chat: *"Explain what this COBOL program does"*
3. Ask: *"Convert this COBOL program to Java"*
4. Show the generated Java — highlight how it creates proper classes, enums, methods
5. Ask: *"Generate unit tests for this Java conversion"*
6. Discuss: "This is one program. For millions of lines, you need a migration
   strategy — but Copilot is the engine that makes each conversion fast and high-quality."
