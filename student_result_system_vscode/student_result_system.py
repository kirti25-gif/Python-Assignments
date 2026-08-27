import logging

# Change this to logging.ERROR to demonstrate ERROR-level logging,
# or logging.DEBUG to record all levels.
LOG_LEVEL = logging.ERROR

logging.basicConfig(
    filename="student_app.log",
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def calculate_average(marks):
    """Calculate and return the average of a list of marks."""
    if not marks:
        raise ZeroDivisionError("Cannot calculate average with no marks.")
    return sum(marks) / len(marks)


def get_result(average):
    """Return the result category based on the average."""
    if 90 <= average <= 100:
        return "Excellent"
    elif 75 <= average < 90:
        return "Very Good"
    elif 50 <= average < 75:
        return "Pass"
    return "Fail"


def get_student_name():
    """Get a non-empty student name."""
    while True:
        name = input("Enter student name: ").strip()
        if name:
            logger.info("Student name received.")
            return name

        logger.warning("Empty student name entered.")
        print("Student name cannot be empty. Please try again.")


def get_number_of_subjects():
    """Get a valid positive integer number of subjects."""
    while True:
        try:
            number = int(input("Enter number of subjects: "))

            if number < 0:
                logger.warning("Negative number of subjects entered.")
                print("Number of subjects cannot be negative.")
                continue

        except ValueError:
            logger.error("Invalid number of subjects entered.")
            print("Please enter a valid number.")
        else:
            logger.debug("Number of subjects accepted: %d", number)
            return number


def get_marks(number_of_subjects):
    """Read and validate marks for every subject."""
    marks = []

    for subject in range(1, number_of_subjects + 1):
        while True:
            try:
                mark = float(input(f"Enter marks for subject {subject}: "))

                if not 0 <= mark <= 100:
                    logger.warning(
                        "Invalid mark %.2f entered for subject %d.", mark, subject
                    )
                    print("Marks must be between 0 and 100.")
                    print("Please enter the marks again.")
                    continue

            except ValueError:
                logger.error("Non-numeric mark entered for subject %d.", subject)
                print("Please enter a valid number for the marks.")
                continue
            else:
                marks.append(mark)
                logger.info("Mark entered successfully for subject %d.", subject)
                break

    return marks


def process_student():
    """Process one student's result."""
    logger.info("Student processing started.")

    try:
        name = get_student_name()
        number_of_subjects = get_number_of_subjects()

        # Intentionally handle zero so the required ZeroDivisionError
        # scenario is demonstrated safely.
        if number_of_subjects == 0:
            logger.warning("Zero subjects entered.")
            try:
                average = calculate_average([])
            except ZeroDivisionError:
                logger.error("Cannot calculate average because subjects are zero.")
                print("Number of subjects must be greater than 0.")
                return
        else:
            marks = get_marks(number_of_subjects)
            average = calculate_average(marks)

            logger.debug("Marks received: %s", marks)
            logger.info("Calculation completed.")

            result = get_result(average)

            print("\n----- Student Result -----")
            print(f"Student Name : {name}")
            print(f"Average : {average:.2f}")
            print(f"Result : {result}")

            print("\n----- Student Statistics -----")
            print(f"Highest Mark : {max(marks):.2f}")
            print(f"Lowest Mark : {min(marks):.2f}")
            print(f"Average Mark : {average:.2f}")
            print(f"Result : {result}")

            logger.info("Student statistics calculated successfully.")

            if average < 50:
                logger.warning("Student average is below the passing mark.")

            logger.info("Student processing completed successfully.")

    except ZeroDivisionError:
        logger.error("ZeroDivisionError occurred during student processing.")
        print("Cannot calculate the average because there are no subjects.")
    except ValueError:
        # Kept as a final safety net; normal input validation handles
        # ValueError closer to the source.
        logger.error("Unexpected ValueError during processing.", exc_info=True)
        print("Invalid input. Please try again.")
    except Exception:
        logger.critical(
            "Unexpected critical failure during student processing.",
            exc_info=True
        )
        print("A serious error occurred. Please check the log file.")
    finally:
        print("Processing completed.")
        logger.debug("Finally block executed.")


def main():
    logger.info("Application started.")

    try:
        while True:
            process_student()

            choice = input("\nDo you want to enter another student? (yes/no): ").strip().lower()

            if choice == "yes":
                logger.info("User chose to process another student.")
                print()
                continue

            if choice == "no":
                logger.info("Application completed.")
                break

            logger.warning("Invalid continuation choice: %s", choice)
            print("Please enter yes or no.")

    except KeyboardInterrupt:
        logger.critical("Application interrupted by user.")
        print("\nApplication interrupted.")
    finally:
        logger.info("Application shutdown completed.")


if __name__ == "__main__":
    main()
