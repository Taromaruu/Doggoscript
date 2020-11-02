import basic
import sys, os
import traceback
import datetime
import random
import platform
import winreg

crash_messages = ["Uh oh...", "Looks like doggo has broke your hopes and dreams", "Boom.", "Look what you have done!", "Pog"]

print("Doggoscript 0.1.5")
print("Docs: https://docs.doggoscript.ml")

def generate_traceback():
    rand = random.choice(crash_messages)
    Registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    with winreg.OpenKey(Registry, "SOFTWARE\Doggo\Doggoscript") as k:
        try:
            ds_ver = winreg.QueryValueEx(k, "Version")[0]
        except FileNotFoundError:
            ds_ver = "Key not found in reg"
    
    x = datetime.datetime.now()
    y = x.strftime("%B-%d-%Y %I-%M-%S %p")
    if not os.path.isdir("crash_logs"):
        os.mkdir("crash_logs")
    with open(f"crash_logs/{y}.log", "w", encoding="utf-8") as f:
        f.write(
f"""--- Begining of crash report ---
// {rand}

Time: {x}
Description: {e}

Full Traceback:\n\n{traceback.format_exc()}

--- System Info ---
Doggoscript Version: {ds_ver}
Python Version: {platform.python_version()}

Node Name: {platform.node()}
Platform: {platform.platform()} {platform.machine()}
Processor: {platform.processor()}
Architecture: {" ".join(platform.architecture())}
""")
    print(f"\nDoggoscript has ran into a exception! Log {y}.log has been created.")

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

        try:
            result, error = basic.run("<stdin>", text)
        except BaseException as e:
            generate_traceback()
            break

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
    except BaseException as e:
        generate_traceback()
        break
