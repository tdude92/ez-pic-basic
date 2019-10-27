def initialize():
    """Returns PIC starting code."""
    code = "TRISB = %00000000\nTRISC = %00000000\nTRISD = %00000000\n"
    return code


def setLED(coords):
    """Takes a three-digit coordinate of an led as a string and returns a list of the two ports needed to light the specified led"""
    coords = coords
    x = int(coords[0])
    y = int(coords[1])
    z = int(coords[2])
    
    pos = [["d3", "d2", "d1", "d0"],
           ["d7", "d6", "d5", "d4"],
           ["b3", "b2", "b1", "b0"],
           ["b7", "b6", "b5", "b4"]] 
    neg = ["c4", "c5", "c6", "c7"]

    return [pos[z][x], neg[y]]

    
def led_ptp(ports):
    """Takes a list of lists of 2 ports (that represent 1 led in the form [b/d port, c port]) and returns one subframes worth of port statements."""
    output = []

    for c in ["c4", "c5", "c6", "c7"]:
        b_ports = ["0", "0", "0", "0", "0", "0", "0", "0"]
        c_ports = ["0", "0", "0", "0", "0", "0", "0", "0"]
        d_ports = ["0", "0", "0", "0", "0", "0", "0", "0"]
        for port in ports:
            if port[1] == c:
                if port[0][0] == "b":
                    b_ports[int(port[0][1])] = "1"
                elif port[0][0] == "d":
                    d_ports[int(port[0][1])] = "1"
        c_ports[int(c[1])] = "1"

    
        b_ports.reverse()
        c_ports.reverse()
        d_ports.reverse()

        b_ports = "".join(b_ports)
        c_ports = "".join(c_ports)
        d_ports = "".join(d_ports)

        portb = "portb=%" + b_ports
        portc = "portc=%" + c_ports
        portd = "portd=%" + d_ports

        if b_ports + d_ports == "00000000" * 2:
            output.append("pause 1")
        else:
            output.extend([portb + "\n" + portc + "\n" + portd, "pause 1"])
    return output


def compile_line(line):
    """Compile a line of the object code"""
    code = ""

    parsed_line = line.split()
    if len(parsed_line) == 0 or parsed_line[0] == "//" or parsed_line[0][0:2] == "//":
        # Since it is a comment or whitespace, don't do anything.
        pass
    elif parsed_line[0] == "LOOP":
        code += parsed_line[1] + " var word\nfor " + parsed_line[1] + " = 1 to " + parsed_line[2] + "\n"
    elif parsed_line[0] == "GOTO":
        code += "next " + parsed_line[1] + "\n"
    else:
        ##################
        # Generate Frame #
        ##################

        # Split LED coordinates and brightness values.
        # Add 1 to brightness to get number of lit frames.
        parsed_line = [i if len(i) == 4 else i + "9" for i in parsed_line]
        leds = [[setLED(i[:3]), int(i[3]) + 1] for i in parsed_line]

        prev_port_statement = ""
        for _ in range(10):
            led_ports = []
            for i in range(len(leds)):
                if leds[i][1] > 0:
                    leds[i][1] -= 1
                    led_ports.append(leds[i][0])
            code += "\n".join(led_ptp(led_ports)) + "\n"
    return code


def clean_file(file_name):
    """Clean a compiled file"""
    with open(file_name, "r") as clean_file:
        # Split input file data into each line and remove whitespace.
        file_content = [i.strip() for i in clean_file.readlines()]
        file_content = [i for i in file_content if i != ""]

        # Combine port statements into subframes.
        while True:
            for i in range(len(file_content)):
                if file_content[i][:5] == "portb" and len(file_content[i]) == 15:
                    file_content[i] = "\n".join(file_content[i:i + 3])
                    del file_content[i + 1]
                    del file_content[i + 1]
                    break
            else:
                break

        # Delete useless port statements.
        while True:
            prev_port_statement = ""
            for i in range(len(file_content)):
                if file_content[i][:5] == "portb":
                    if file_content[i] == prev_port_statement:
                        del file_content[i]
                        break
                    else:
                        prev_port_statement = file_content[i]
            else:
                break
        
        # Merge consecutive pause statements.
        while True:
            for i in range(1, len(file_content)):
                if file_content[i - 1][:5] == file_content[i][:5] == "pause":
                    file_content[i] = file_content[i][:6] + str(int(file_content[i][6:]) + int(file_content[i - 1][6:]))
                    del file_content[i - 1]
                    break
            else:
                break

    with open(file_name, "w") as clean_file:
        clean_file.write("\n".join(file_content))


def compile_file(file_name):
    """Compile an entire file"""
    with open(file_name, "r") as input_file:
        # Split input file data into each line.
        parsed_input = [i.strip() for i in input_file.readlines()]
    
    output_name = file_name.split(".", 1)[0] + ".picb"
    with open(output_name, "w+") as output_file:
        output_file.write(initialize())
        for line in parsed_input:
            output_file.write(compile_line(line))
    clean_file(output_name)
