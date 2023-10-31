@echo off

..\..\compile\ML.EXE /I. /Zm /c /Ta main.asm
..\..\compile\ML.EXE /I. /Zm /c /Ta input.asm
..\..\compile\ML.EXE /I. /Zm /c /Ta output.asm
..\..\compile\ML.EXE /I. /Zm /c /Ta calc.asm

..\..\compile\LINK.EXE main.obj input.obj output.obj calc.obj
