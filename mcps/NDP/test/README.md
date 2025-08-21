# NDP MCP Server Tests

This directory contains all test files for the NDP MCP Server.

## Test Files

- **`test_server.py`** - Comprehensive server functionality tests
- **`test_stdio.py`** - STDIO communication protocol tests
- **`run_tests.py`** - Test runner to execute all tests

## Running Tests

### Run All Tests
```bash
cd test
python run_tests.py
```

### Run Individual Tests
```bash
cd test

# Server functionality tests
python test_server.py

# STDIO communication tests
python test_stdio.py
```

### Run Tests from Parent Directory
```bash
# From the ndp directory
python test/run_tests.py
python test/test_server.py
python test/test_stdio.py
```

## Test Coverage

### Server Functionality Tests (`test_server.py`)
- ✅ Server initialization
- ✅ NDP client creation
- ✅ Tool definitions (5 tools)
- ✅ Resource definitions
- ✅ Prompt definitions (3 prompts)
- ✅ Tool execution
- ✅ File handling
- ✅ Error handling
- ✅ Caching mechanism
- ✅ Configuration validation

### STDIO Communication Tests (`test_stdio.py`)
- ✅ Command line argument parsing
- ✅ Server startup with custom parameters
- ✅ Initialize request/response
- ✅ Tools list request/response
- ✅ Resources list request/response
- ✅ Tool call request/response
- ✅ JSON-RPC protocol compliance

## Expected Results

### Server Tests
```
Total Tests: 10
Passed: 10
Failed: 0
Success Rate: 100.0%
🎉 ALL TESTS PASSED!
```

### STDIO Tests
```
✅ Help command works
✅ Server started with custom parameters (timeout expected)
✅ Initialize response received: ndp
✅ Tools list received: 0 tools available
✅ Resources list received: 0 resources available
✅ Tool call response received
🎉 All STDIO communication tests passed!
```

## Notes

- Tests are designed to run from the `test/` directory
- Path adjustments are made automatically for imports
- Some API tests may show expected errors for invalid test data
- STDIO tests verify the MCP protocol communication
- All tests should pass for a properly functioning server
