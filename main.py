import random
import string


def get_user_preferences():

    while True:
        try:
            length = int(input("Enter desired password length: "))
            if length <= 0:
                print("Password length must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    include_upper = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    include_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
    include_special = input("Include special characters? (y/n): ").strip().lower() == 'y'

    return length, include_upper, include_numbers, include_special


def generate_password(length, include_upper, include_numbers, include_special):


    chars = list(string.ascii_lowercase)


    if include_upper:
        chars += list(string.ascii_uppercase)
    if include_numbers:
        chars += list(string.digits)
    if include_special:
        chars += list(string.punctuation)


    if not chars:
        raise ValueError("No character sets selected. Cannot generate password.")

    password = ''.join(random.choice(chars) for _ in range(length))
    return password


def main():
    print("\n === Secure Password Generator === \n")


    length, include_upper, include_numbers, include_special = get_user_preferences()


    password = generate_password(length, include_upper, include_numbers, include_special)

    print("\n Your Generated Password:")
    print(password)



def run_tests():

    print("\n Running basic tests...")


    assert len(generate_password(8, True, True, True)) == 8
    assert len(generate_password(1, False, False, False)) == 1
    assert len(generate_password(20, True, False, False)) == 20


    try:
        generate_password(10, False, False, False)
    except ValueError:
        print("Caught expected ValueError for no character types.")


    pw = generate_password(1000, True, True, True)
    assert len(pw) == 1000

    print("All tests passed successfully!")


if __name__ == "__main__":
    # Run main program
    main()


    run_tests()
