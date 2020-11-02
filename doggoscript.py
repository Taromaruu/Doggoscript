import basic
import sys

print("Doggoscript 0.1.5")
print("Docs: https://docs.doggoscript.ml")

while True:
    try:
        result, error = basic.run("<stdin>", f"run(\"{sys.argv[1]}\")")

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
        break
    except IndexError:
        try:
            text = input("DoggoScript >>> ")
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        result, error = basic.run("<stdin>", text)

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))