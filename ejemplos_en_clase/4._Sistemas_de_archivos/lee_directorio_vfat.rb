#!/usr/bin/ruby
# coding: utf-8
filename='/dev/mmcblk0p1'
offset = '0x2a000'.to_i(16)
fh = open(filename, 'r')

fh.seek(offset)
100.times do
  data = fh.read(32)
  archivo=data[0..7]
  ext = data[8..10]
  if data[11] == ' ' # 20 en hexadecimal → 32 decimal; 32.chr ⇒ ' '
    puts '→ ' + archivo + '.' + ext
  elsif data[11] == '0x10'.to_i(16).chr
    puts '⇒ ' + archivo + '.' + ext + ' (DIRECTORIO)'
  else
    puts '  ' +  archivo + ext + '(... entrada vfat ↓ ...)'
  end
end
