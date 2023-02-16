if __name__ == '__main__':
    ss = SerialComm(port='/dev/ttyACM0', baudrate=115200)

    while True:
        ss.serial_command = '1'
        print(f">>>APP: {ss.get_value()}")
        ss.serial_command = '2'
        print(f">>>APP: {ss.get_value()}")
