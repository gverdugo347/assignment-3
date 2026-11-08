import sqlite3

with sqlite3.connect('concrete.db') as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. SHOW ALL TESTS
    print("\nALL TESTS")
    cursor.execute('''
    SELECT project_name, actual_strength, passed
    FROM concrete_tests
    ORDER BY test_id
    ''')

    while row := cursor.fetchone():
        if row['passed'] == 1:
            result = "PASS"
        else:
            result = "FAIL"
        print(f"{row['project_name']}: {row['actual_strength']} PSI - {result}")
    
    # 2. Show ONLY failed tests
    print("\nFAILED TESTS")
    cursor.execute('''
        SELECT project_name, test_date, required_strength, actual_strength
        FROM concrete_tests
        WHERE passed = 0
        ORDER BY test_id
        ''')
    while row := cursor.fetchone():
        print(f"{row['project_name']} on {row['test_date']}")
        print(f"Required: {row['required_strength']} PSI")
        print(f"Actual: {row['actual_strength']} PSI")
        print("\n")

    # 3. Count tests by project
    print("TESTS PER PROJECT")
    cursor.execute('''
        SELECT project_name,
          COUNT(*) AS total_tests,
          SUM(passed) AS passed_tests
        FROM concrete_tests
        GROUP BY project_name
        ORDER BY project_name
        ''')
    while row := cursor.fetchone():
        print(f"{row['project_name']}: {row['passed_tests']}/{row['total_tests']} passed")