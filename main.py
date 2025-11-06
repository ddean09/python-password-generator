import secrets
import string

def get_user_preferences():
    while True:
        try:
            length = int(input("Enter desired password length (minimum 8): "))
            if length < 8:
                print("Password length must be at least 8.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    include_upper = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    include_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
    include_special = input("Include special characters? (y/n): ").strip().lower() == 'y'

    if not any([include_upper, include_numbers, include_special]):
        print("Warning: No additional character types selected. Password will be lowercase only.")

    return length, include_upper, include_numbers, include_special

def generate_password(length, include_upper, include_numbers, include_special):

    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase) if include_upper else []
    numbers = list(string.digits) if include_numbers else []
    special = list(string.punctuation) if include_special else []

    all_chars = lowercase + uppercase + numbers + special
    if not all_chars:
        raise ValueError("No character sets available to generate password.")


    password_chars = []
    if uppercase:
        password_chars.append(secrets.choice(uppercase))
    if numbers:
        password_chars.append(secrets.choice(numbers))
    if special:
        password_chars.append(secrets.choice(special))


    remaining_length = length - len(password_chars)
    password_chars += [secrets.choice(all_chars) for _ in range(remaining_length)]


    secrets.SystemRandom().shuffle(password_chars)

    return ''.join(password_chars)

def main():
    print("\n=== Secure Password Generator ===\n")
    length, include_upper, include_numbers, include_special = get_user_preferences()
    password = generate_password(length, include_upper, include_numbers, include_special)
    print("\nYour Generated Password:")
    print(password)

def run_tests():
    print("\nRunning basic tests...")
    # Basic length tests
    assert len(generate_password(8, True, True, True)) == 8
    assert len(generate_password(12, False, False, False)) == 12
    assert len(generate_password(20, True, False, False)) == 20


    try:
        generate_password(10, False, False, False)
    except ValueError:
        print("Caught expected ValueError for no character types.")


    pw = generate_password(1000, True, True, True)
    assert len(pw) == 1000

    print("All tests passed successfully!")

if __name__ == "__main__":
    main()
    run_tests()
