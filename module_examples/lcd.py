from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander="PCF8574", address=0x27, port=1, cols=20, rows=4, dotsize=8)
lcd.clear()

lcd.write_string("Please enter string\r\n\r\n")
lcd.write_string("Hello World!")


while True:
    input_str = input("Enter string: ")
    lcd.clear()
    # lcd.write_string("Please enter string\r\n\r\n")
    lcd.write_string(input_str)
