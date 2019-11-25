r0 = 1
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0


def begin():
    r1 = 1
    r4 = 1          # 2 ; loop (intil r4 == r2)

    while r2 != r4:
        r3 = r1 * r4    # 3 ; r3 = r1 * r4 (r1 is 1, so r3 = r4)

        #r3 = r3 == r2   # 4 ; r3 = r3 == r2
        #r5 = r3 + r5    # 5 ; if (r3 == r2) skip next instruction
        #r5 = r5 + 1     # 6 ; skip next instruction

        if r3 == r2:
            r0 = r1 + r0    # 7 ; add r1 to r0
        r4 = r4 + 1     # 8 ; add 1 to r4 
        #r3 = r4 == r2   # 9 ; r3 is 1 if r4 == r2
        #r5 = r5 + r3    # 10 ; jump r5 + r3 (r3 usually is 0, so nothing)
        #r5 = 2          # 11 ; jump back to label 'loop'

    r1 = r1 + 1     # 12 ; add 1 to r1
    r3 = r1 > r2    # 13
    r5 = r3 + r4    # 14 ; end program
    r5 = 1          # 15 ; set ir to 1
    r5 = r5 * r5    # 16 ; jump out of bounds (r5 = 16, so 16*16 is halt)


def init():
    r2 = r2 + 2   # 17
    r2 = r2 * r2  # 18
    r2 = 19 * r2  # 19, r5 = 19
    r2 = r2 * 11 # 20
    r3 = r3 + 8 # 21
    r3 = r3 * r5 # 22
    r3 = r3 + 16 # 23
    r2 = r2 + r3 # 24
    #25: r5 = r5 + r0    ; jump to r5 + r0
    #26: r5 = 0          ; jump to 0+1 = 1 (label: begin)
    if r0 == 1:
        r3 = 27         # 27 ; r3 = 27
        r3 = r3 * 28    # 28 ; r3 = 27 * 28
        r3 = 29 + r3    # 29 ; r3 = 29 + (27 * 28)
        r3 = 30 * r3    # 30 ; r3 = 30 * (29 + (27 * 28))
        r3 = r3 * 14    # 31 ; r3 = (30 * (29 + (27 * 28))) * 14
        r3 = r3 * 32    # 32 ; r3 = ((30 * (29 + (27 * 28))) * 14) * 32
        r2 = r2 + r3    # 33
        r0 = 0          # 34
        r5 = 0          # 35 ; jump to 0+1 = 1 (label: begin)
    begin()

r0 = 1
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0

init() # line 0
