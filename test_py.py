
import sqlite3
import subprocess
import pickle
import hashlib

# VULNERABILITY 1: Hardcoded credentials
API_KEY = "test_secret_key_123456"
DATABASE_PASSWORD = "admin123"

# VULNERABILITY 2: SQL injection
def get_user(username):
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE users (username TEXT, role TEXT)"
    )
    cursor.execute(
        "INSERT INTO users VALUES ('alice', 'user')"
    )

    # Vulnerable: user input is concatenated into SQL
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    result = cursor.fetchall()
    connection.close()
    return result


# VULNERABILITY 3: Command injection
def check_file(filename):
    # Vulnerable: untrusted input is passed to a shell
    command = "ls " + filename
    return subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )


# VULNERABILITY 4: Insecure deserialization
def load_data(serialized_data):
    # Vulnerable: never unpickle untrusted data
    return pickle.loads(serialized_data)


# VULNERABILITY 5: Weak hashing algorithm
def hash_password(password):
    # Vulnerable: MD5 is unsuitable for password storage
    return hashlib.md5(password.encode()).hexdigest()


if __name__ == "__main__":
    print("SAST security test file")
    print("User lookup:", get_user("alice"))
    print("Password hash:", hash_password("example-password"))
