from communication.com_serial import SerialComm

if __name__ == '__main__':
    ss = SerialComm(port='/dev/ttyACM0', baudrate=115200)

    while True:
        ss.serial_command = '1'
        print(f">>>APP: {ss.send_query()}")
        ss.serial_command = '2'
        print(f">>>APP: {ss.send_query()}")
