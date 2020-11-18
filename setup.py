from cx_Freeze import setup, Executable
setup(
    name="Doggoscript",
    version="0.1",
    description="Doggoscript",
    executables=[Executable("doggoscript.py", base="Console")],
    )