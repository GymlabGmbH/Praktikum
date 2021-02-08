def DisplayScrollingLeft(txt):
  txt = txt.strip() + ' '
  if len(txt) < 17:
    txt = txt + (16 * ' ' )
  while True:
     lcd.set_cursor(0, 0)
     lcd.message(txt[:16])
     lcd.set_cursor(0, 1)
     lcd.message(datetime.now().strftime('%b %d  %H:%M:%S'))
     time.sleep(0.5)
     txt = txt[1:] + txt[0]

DisplayScrollingLeft('This scrolls to the left.')