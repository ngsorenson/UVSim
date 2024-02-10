| Use Case | Unit Test Name                               | Description                                          | Inputs            | Expected Outputs     |
|----------|----------------------------------------------|------------------------------------------------------|-------------------|----------------------|
| 4        | test_add_success                            | Perform addition successfully                        | ADD(1010, 101)    | 1111                 |
| 4        | test_add_fail                               | Addition fails due to invalid accumulator type      | ADD("1010", 101)  | TypeError            |
| 5        | test_subtract_success                       | Perform subtraction successfully                     | SUBTRACT(1111, 101) | 1010               |
| 5        | test_subtract_fail                          | Subtraction fails due to invalid value type        | SUBTRACT(1111, 101.1) | TypeError         |
| 6        | test_multiply_success                       | Perform multiplication successfully                  | MULTIPLY(1010, 5) | 5050                 |
| 6        | test_multiply_fail                          | Multiplication fails due to invalid value type     | MULTIPLY(1010, "5") | TypeError            |
| 7        | test_divide_success                         | Perform division successfully                       | DIVIDE(5050, 5)   | 1010                 |
| 7        | test_divide_fail                            | Division fails due to invalid accumulator type     | DIVIDE(5050.3, 5) | TypeError            |
| 7        | test_divide_by_zero                        | Division fails due to division by zero             | DIVIDE(1010, 0)   | ZeroDivisionError    |
| 2        | test_read_success                           | Positive test for READ instruction                  | READ(99)          | 1337 (in memory)     |
| 2        | test_read_fail                              | Negative test for READ instruction                  | READ(10)          | SystemExit           |
| 9        | test_write_success                          | Positive test for WRITE instruction (write to memory) | (To be determined) | (To be determined) |
| 9        | test_write_fail                             | Negative test for WRITE instruction (invalid data type) | (To be determined) | (To be determined) |
| 10       | test_load_success                           | Positive test for LOAD instruction (load from memory) | (To be determined) | (To be determined) |
| 10       | test_load_fail                              | Negative test for LOAD instruction (invalid data type) | (To be determined) | (To be determined) |
| 11       | test_store_success                          | Positive test for STORE instruction (store in memory) | (To be determined) | (To be determined) |
| 11       | test_store_fail                             | Negative test for STORE instruction (invalid data type) | (To be determined) | (To be determined) |
| 1        | test_store_program_in_memory_success       | Load program into memory successfully               | "Test1.txt"      | (To be determined)   |
| 1        | test_store_program_in_memory_failure       | Load program into memory failure (file not found)   | "Failure.txt"    | FileNotFoundError   |
| 3        | test_run_program_success                   | Run program successfully                            | (To be determined) | (To be determined) |
| 3        | test_run_program_failure                   | Run program failure (handling EOFError)             | (To be determined) | EOFError             |
