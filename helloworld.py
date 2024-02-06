import sys

def format_name(name):
    # Methode zum Konvertieren des Namens in Großbuchstaben
    return name.upper()

def main():
    # Überprüfen, ob ein Parameter übergeben wurde
    if len(sys.argv) > 1:
        # Wenn ja, den ersten Parameter (Index 1) verwenden und in Großbuchstaben umwandeln
        name = format_name(sys.argv[1])
    else:
        # Wenn kein Parameter übergeben wurde, den Standardnamen "JOE DOE" verwenden
        name = format_name("JOE DOE")

    # Den formatierten Namen ausgeben
    print(f"Der formatierte Name ist: {name}")

if __name__ == "__main__":
    main()
